"""Validate Phase 1 documentation with Python standard library only.

This is a documentation consistency check, not an application or model test.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "docs/repository-assessment.md",
    "docs/requirements.md",
    "docs/taxonomy-spec.md",
    "docs/classification-policy.md",
    "docs/data-contract.md",
    "docs/annotation-guideline.md",
    "docs/api-contract.md",
    "docs/database-design.md",
    "docs/model-evaluation-plan.md",
    "docs/quality-slo.md",
    "docs/data-governance.md",
    "docs/security-threat-model.md",
    "docs/architecture-design.md",
    "docs/risk-register.md",
    "docs/phase-status.md",
    "docs/phase-1-acceptance.md",
    "docs/phase-2-backlog.md",
    "docs/verification-runbook.md",
    "docs/decisions/ADR-001-classification-cardinality.md",
    "docs/decisions/ADR-002-taxonomy-lifecycle.md",
    "docs/decisions/ADR-003-data-governance-deployment.md",
    "docs/decisions/ADR-004-evaluation-and-quality-gates.md",
    "docs/decisions/ADR-005-api-idempotency.md",
    "docs/decisions/ADR-006-persistence-transaction-audit.md",
    "docs/decisions/ADR-007-model-runtime-selection.md",
)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SENSITIVE_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
)
EXPECTED_MARKER = "PHASE_1_IMPLEMENTED_AWAITING_VERIFICATION"


def validate() -> list[str]:
    errors: list[str] = []
    for name in REQUIRED:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Missing required file: {name}")
            continue
        content = path.read_text(encoding="utf-8")
        if not content.strip():
            errors.append(f"Empty required file: {name}")
        if name.endswith(".md"):
            if content.count("~~~") % 2:
                errors.append(f"Unbalanced fenced section: {name}")
            for match in LINK_PATTERN.finditer(content):
                target = unquote(match.group(1).split("#", 1)[0].strip())
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                linked = (path.parent / target).resolve()
                if not linked.is_relative_to(ROOT) or not linked.exists():
                    errors.append(f"Broken local link: {name} -> {target}")
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(content):
                errors.append(f"Potential credential pattern in {name}")
    marker = ROOT / "docs/phase-status.md"
    if marker.is_file() and EXPECTED_MARKER not in marker.read_text(encoding="utf-8"):
        errors.append("Unexpected Phase 1 marker")
    for name in REQUIRED:
        if name.startswith("docs/decisions/") and (ROOT / name).is_file():
            text = (ROOT / name).read_text(encoding="utf-8")
            if "NOT APPROVED" not in text:
                errors.append(f"ADR lacks explicit unapproved state: {name}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for issue in problems:
            print("FAIL:", issue)
        sys.exit(1)
    print(f"PASS: {len(REQUIRED)} required files, links, ADR status, marker, and basic sensitive-pattern checks")
