import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("scan_public_safety.py")
SPEC = importlib.util.spec_from_file_location("scan_public_safety", MODULE_PATH)
assert SPEC and SPEC.loader
scanner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scanner)


def test_safe_synthetic_text_passes() -> None:
    assert scanner.scan_text("Northstar Demo uses local-synthetic-demo-token.") == []


def test_private_indicators_are_redacted_from_output() -> None:
    fixture = "person@example.com AKIAABCDEFGHIJKLMNOP"  # safety-test-fixture
    findings = scanner.scan_text(fixture)
    assert findings == [("email", 1), ("cloud-key", 1)]


def test_private_source_names_are_rejected() -> None:
    fixture = "whatsapp-ai-agent-platform-current"  # safety-test-fixture
    assert scanner.scan_text(fixture) == [("forbidden-source-name", 1)]
