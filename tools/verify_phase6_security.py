"""Bounded source hygiene check. Not a comprehensive credential/security audit."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SIGNATURES = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "literal_postgres_password": re.compile(
        r"postgresql\+asyncpg://[^\s/:\"@]+:[^\s/\"@$({]+@",
        re.IGNORECASE,
    ),
}

def detect_signatures(source: str) -> tuple[str, ...]:
    """Return only rule IDs; never reveal source fragments or credentials."""
    return tuple(name for name, pattern in SIGNATURES.items() if pattern.search(source))

def source_paths() -> list[Path]:
    candidates = list((ROOT / "src").rglob("*.py"))
    candidates += list((ROOT / "src" / "host" / "res").glob("*.yaml"))
    candidates += [ROOT / "Dockerfile", ROOT / "compose.yaml"]
    candidates += [ROOT / "deploy" / "compose.staging.yaml"]
    candidates += list((ROOT / ".github" / "workflows").glob("*.yml"))
    return sorted(path for path in candidates if path.is_file())

def main() -> int:
    failures = []
    paths = source_paths()
    for path in paths:
        for name in detect_signatures(path.read_text(encoding="utf-8")):
            failures.append((str(path.relative_to(ROOT)), name))
    if failures:
        for path, name in failures:
            print(f"FAIL: {path}: {name} signature (value intentionally omitted)")
        return 1
    print(f"PASS: bounded source signature scan ({len(paths)} files); not a full secret audit")
    return 0

if __name__ == "__main__":
    sys.exit(main())
