"""Phase 6 independent security hygiene tests; no real secrets or employer data."""
from tools.verify_phase6_security import detect_signatures, source_paths


def test_secret_signature_detector_does_not_echo_values():
    samples = (
        ("AKIA" + "A" * 16, "aws_access_key"),
        ("ghp_" + "Z" * 36, "github_token"),
        ("postgresql+asyncpg://user:example_secret@example.test/db", "literal_postgres_password"),
        ("-----BEGIN PRIVATE KEY-----", "private_key"),
    )
    for raw, expected_rule in samples:
        result = detect_signatures(raw)
        assert expected_rule in result
        assert raw not in repr(result)


def test_phase6_source_scanner_has_no_false_dependency_on_test_fixtures():
    paths = source_paths()
    assert paths
    assert all(path.is_file() for path in paths)
    assert all("tests" not in path.parts for path in paths)


def test_environment_reference_is_not_a_hardcoded_secret():
    assert detect_signatures("DATABASE_URL=${COMPOSE_DATABASE_URL:?required}") == ()
