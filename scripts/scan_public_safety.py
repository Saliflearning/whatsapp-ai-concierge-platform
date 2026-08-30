#!/usr/bin/env python3
"""Fail closed when public tracked text contains likely private or secret material."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SKIP_PARTS = {
    ".git",
    ".next",
    ".venv",
    "node_modules",
    "node_modules.partial",
    "graphify-out",
}
TEXT_SUFFIXES = {
    ".css",
    ".env",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
PRIVATE_PATH_PATTERN = (
    r"(?:[A-Z]:\\Users\\|/Users/|/home/)[^\s'\"]+"  # safety-test-fixture
)
PRIVATE_SOURCE_PATTERN = (  # safety-test-fixture
    r"Realtor-whatsapp-ai-agent-|whatsapp-ai-agent-platform-current"  # safety-test-fixture
)

PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "phone": re.compile(
        r"(?<!\w)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\w)"
    ),
    "private-path": re.compile(PRIVATE_PATH_PATTERN, re.IGNORECASE),
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "cloud-key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    "generic-secret": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token)\b\s*[:=]\s*['\"][^'\"]{12,}['\"]"
    ),
    "forbidden-source-name": re.compile(PRIVATE_SOURCE_PATTERN, re.IGNORECASE),
}


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [root / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def text_files(root: Path) -> list[Path]:
    if (root / ".git").exists():
        return tracked_files(root)
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and not any(part in SKIP_PARTS for part in path.parts)
        and (path.suffix.lower() in TEXT_SUFFIXES or path.name == ".env.example")
    ]


def scan_text(text: str) -> list[tuple[str, int]]:
    findings: list[tuple[str, int]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if "safety-test-fixture" in line:
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append((label, line_number))
    return findings


def scan_current(root: Path) -> list[str]:
    findings: list[str] = []
    for path in text_files(root):
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        findings.extend(
            f"{path.relative_to(root)}:{line_number}:{label}"
            for label, line_number in scan_text(content)
        )
    return sorted(findings)


def scan_history(root: Path) -> list[str]:
    revisions = subprocess.run(
        ["git", "rev-list", "--all"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    findings: list[str] = []
    for revision in revisions:
        listing = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", revision],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        for name in listing:
            if (
                Path(name).suffix.lower() not in TEXT_SUFFIXES
                and Path(name).name != ".env.example"
            ):
                continue
            blob = subprocess.run(
                ["git", "show", f"{revision}:{name}"],
                cwd=root,
                check=False,
                capture_output=True,
            )
            if blob.returncode or b"\0" in blob.stdout:
                continue
            try:
                content = blob.stdout.decode("utf-8")
            except UnicodeDecodeError:
                continue
            findings.extend(
                f"{revision[:12]}:{name}:{line_number}:{label}"
                for label, line_number in scan_text(content)
            )
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--history", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    findings = scan_history(root) if args.history else scan_current(root)
    if findings:
        print(
            f"Public safety scan failed with {len(findings)} finding(s):",
            file=sys.stderr,
        )
        print("\n".join(findings), file=sys.stderr)
        return 1
    print(
        f"Public safety scan passed ({'history' if args.history else 'current tree'})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
