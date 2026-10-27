"""Fail-closed shape checks for API-only shared-host staging; no deployment actions.

This verifies local staging configuration, NOT server health, TLS handshakes,
model readiness, secret provenance, or approval to deploy.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "deploy" / "compose.staging.yaml"
DIGEST = re.compile(r"^[a-zA-Z0-9._:/-]+@sha256:[a-fA-F0-9]{64}$")
MEMORY = re.compile(r"^[1-9][0-9]*[mMgG]$")


class PreflightError(ValueError):
    """Non-secret staging configuration failure."""


def verify_profile(path: Path = PROFILE) -> None:
    """Reject accidental DB/vLLM duplication and public API exposure."""
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise PreflightError("Staging Compose profile unavailable or invalid") from exc
    if not isinstance(document, dict) or document.get("name") != "text-classification-service-staging":
        raise PreflightError("Expected dedicated staging project name")
    services = document.get("services")
    if not isinstance(services, dict) or set(services) != {"api"}:
        raise PreflightError("Staging must contain only its own API service")
    api = services["api"]
    if not isinstance(api, dict):
        raise PreflightError("API service configuration missing")
    required = {
        "image": "${TCS_STAGING_IMAGE:?Provide an approved immutable image digest}",
        "ports": ["127.0.0.1:${TCS_STAGING_PORT:?Choose an unused non-8000 localhost port}:8000"],
        "networks": ["shared_db"],
        "read_only": True,
        "cap_drop": ["ALL"],
        "security_opt": ["no-new-privileges:true"],
        "pids_limit": "${TCS_STAGING_PIDS:?Set an Ops-approved process limit}",
        "cpus": "${TCS_STAGING_CPUS:?Set an Ops-approved CPU limit}",
        "mem_limit": "${TCS_STAGING_MEMORY:?Set an Ops-approved RAM limit}",
        "restart": "unless-stopped",
    }
    for key, value in required.items():
        if api.get(key) != value:
            raise PreflightError("Staging service invariant violated: " + key)
    if api.get("env_file") != ["${TCS_STAGING_ENV_FILE:?Provide an absolute, uncommitted staging environment file}"]:
        raise PreflightError("Staging must use an external environment file")
    if api.get("environment") != {"ENV_TYPE": "production", "PGSSLROOTCERT": "/run/certs/postgres-ca.pem"}:
        raise PreflightError("Production config and CA path are mandatory")
    volumes = api.get("volumes")
    if volumes != [{
        "type": "bind",
        "source": "${TCS_STAGING_DB_CA_FILE:?Provide the approved PostgreSQL CA certificate path}",
        "target": "/run/certs/postgres-ca.pem",
        "read_only": True,
    }]:
        raise PreflightError("Approved CA bind mount required")
    if api.get("privileged") is not None or api.get("devices") is not None or api.get("build") is not None:
        raise PreflightError("No privileged access, GPU or unreviewed local build")
    networks = document.get("networks")
    if networks != {"shared_db": {"external": True, "name": "simorgh-db-net"}}:
        raise PreflightError("Only existing shared PostgreSQL network is allowed")
    health = api.get("healthcheck", {}).get("test", [])
    if not isinstance(health, list) or not any(isinstance(x, str) and "X-Readiness-Scope" in x for x in health):
        raise PreflightError("DB-only readiness scope required")


def verify_runtime(env: dict[str, str] | None = None, *, root: Path = ROOT) -> None:
    """Validate operator-supplied shape without revealing values or contacting services."""
    values = os.environ if env is None else env
    image = values.get("TCS_STAGING_IMAGE", "")
    if not DIGEST.fullmatch(image):
        raise PreflightError("Image must be pinned to a sha256 digest")
    port = values.get("TCS_STAGING_PORT", "")
    if not port.isascii() or not port.isdecimal() or not (1024 <= int(port) <= 65535) or int(port) == 8000:
        raise PreflightError("Staging host port must be non-8000 and unprivileged")
    for key in ("TCS_STAGING_ENV_FILE", "TCS_STAGING_DB_CA_FILE"):
        value = values.get(key, "")
        candidate = Path(value)
        if not candidate.is_absolute() or not candidate.is_file() or candidate.is_relative_to(root):
            raise PreflightError("Approved external environment and CA files must exist outside checkout")
        if key == "TCS_STAGING_ENV_FILE" and (candidate.stat().st_mode & 0o077):
            raise PreflightError("Staging environment file must not be group/world-accessible")
    cpu = values.get("TCS_STAGING_CPUS", "")
    try:
        parsed_cpu = float(cpu)
    except ValueError:
        raise PreflightError("CPU limit must be positive") from None
    if not 0 < parsed_cpu < float("inf"):
        raise PreflightError("CPU limit must be finite and positive")
    if not MEMORY.fullmatch(values.get("TCS_STAGING_MEMORY", "")):
        raise PreflightError("Memory limit must use a positive m/g suffix")
    pids = values.get("TCS_STAGING_PIDS", "")
    if not pids.isascii() or not pids.isdecimal() or int(pids) <= 0:
        raise PreflightError("Process limit must be positive")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check staging profile without deploying")
    parser.add_argument("--runtime", action="store_true", help="Validate server-provided environment shape without printing values")
    args = parser.parse_args(argv)
    try:
        verify_profile()
        if args.runtime:
            verify_runtime()
    except PreflightError as exc:
        print("BLOCKED: " + str(exc))
        return 1
    print("PASS: safe staging profile invariants" + (" and runtime input shape" if args.runtime else ""))
    print("NOTE: live server, PostgreSQL TLS and production acceptance NOT VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
