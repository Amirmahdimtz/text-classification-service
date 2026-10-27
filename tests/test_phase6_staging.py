"""Offline staging safety tests; no Docker, database, secrets, GPU or network."""
from pathlib import Path

import pytest
import yaml

from tools.verify_stage_config import PreflightError, verify_profile, verify_runtime


def test_shared_host_profile_is_api_only_and_private():
    verify_profile()


def test_preflight_rejects_extra_postgres_service(tmp_path):
    from tools.verify_stage_config import PROFILE
    contents = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    contents["services"]["db"] = {"image": "postgres:17"}
    path = tmp_path / "unsafe.yaml"
    path.write_text(yaml.safe_dump(contents), encoding="utf-8")
    with pytest.raises(PreflightError, match="only its own API"):
        verify_profile(path)


def test_runtime_defaults_fail_closed():
    with pytest.raises(PreflightError, match="sha256 digest"):
        verify_runtime({}, root=Path.cwd())


def test_runtime_rejects_vllm_host_port_and_unpinned_image(tmp_path):
    private_env = tmp_path / "staging.env"
    private_env.write_text("ENV_TYPE=production\n", encoding="utf-8")
    private_env.chmod(0o600)
    ca = tmp_path / "postgres-ca.pem"
    ca.write_text("Test-only non-secret fixture\n", encoding="utf-8")
    params = {
        "TCS_STAGING_IMAGE": "registry.example.test/tcs@sha256:" + "a" * 64,
        "TCS_STAGING_PORT": "8000",
        "TCS_STAGING_ENV_FILE": str(private_env),
        "TCS_STAGING_DB_CA_FILE": str(ca),
        "TCS_STAGING_CPUS": "1.0",
        "TCS_STAGING_MEMORY": "512m",
        "TCS_STAGING_PIDS": "50",
    }
    with pytest.raises(PreflightError, match="non-8000"):
        verify_runtime(params, root=Path.cwd())
    params["TCS_STAGING_PORT"] = "18487"
    verify_runtime(params, root=Path.cwd())
    params["TCS_STAGING_IMAGE"] = "registry.example.test/tcs:latest"
    with pytest.raises(PreflightError, match="sha256 digest"):
        verify_runtime(params, root=Path.cwd())
