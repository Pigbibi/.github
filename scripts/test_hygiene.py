#!/usr/bin/env python3
"""Tests for scripts/check_hygiene.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent / "check_hygiene.py"
sys.path.insert(0, str(SCRIPT_PATH.parent))
import check_hygiene as hygiene  # noqa: E402


class CheckHygieneTests(unittest.TestCase):
    def _init_repo(self, root: Path, *, public: bool = False) -> None:
        root.mkdir(parents=True, exist_ok=True)
        agents = "\n".join(
            ["<!-- content-boundary:begin -->"]
            + [f"## {s}\nOK" for s in hygiene.AGENTS_SECTIONS_EN]
        )
        (root / "AGENTS.md").write_text(agents + "\n", encoding="utf-8")
        (root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
        (root / "SECURITY.md").write_text("# Security\n\nPrivate report.\n", encoding="utf-8")
        (root / ".gitignore").write_text(
            "\n".join(hygiene.REQUIRED_GITIGNORE_PATTERNS) + "\n",
            encoding="utf-8",
        )
        if public:
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")
            (root / "CODE_OF_CONDUCT.md").write_text("# Code of Conduct\n", encoding="utf-8")
            (root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True, exist_ok=True)
            (root / ".github" / "ISSUE_TEMPLATE" / "bug.yml").write_text("name: Bug\n", encoding="utf-8")
            (root / ".github" / "pull_request_template.md").write_text("## Summary\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)

    def _run(self, root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--root", str(root), *extra],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_tracked_forbidden_file_fails_even_in_private_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            self._init_repo(root)
            (root / "docs").mkdir(exist_ok=True)
            (root / "docs" / "acceptance-policy.md").write_text("# Internal\n", encoding="utf-8")
            subprocess.run(["git", "add", "-f", "docs/acceptance-policy.md"], cwd=root, check=True)
            res = self._run(root, "--private", "--strict")
            self.assertEqual(res.returncode, 1)
            self.assertIn("docs/acceptance-policy.md: internal artifact must not be tracked in Git", res.stdout)

    def test_english_only_flag_rejects_zh_cn_docs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            self._init_repo(root)
            (root / "README.md").write_text("# Demo\n\n[中文](README.zh-CN.md)\n", encoding="utf-8")
            (root / "README.zh-CN.md").write_text("# Demo\n\n[EN](README.md)\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md", "README.zh-CN.md"], cwd=root, check=True)
            ok = self._run(root, "--private", "--strict")
            self.assertEqual(ok.returncode, 0, msg=ok.stdout)
            fail = self._run(root, "--private", "--strict", "--english-only")
            self.assertEqual(fail.returncode, 1)
            self.assertIn("README.zh-CN.md: .zh-CN.md files are retired", fail.stdout)

    def test_long_list_item_warns_under_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            self._init_repo(root)
            (root / "docs").mkdir(exist_ok=True)
            (root / "docs" / "architecture.md").write_text(
                "# Arch\n\n- " + ("word " * 180) + "\n", encoding="utf-8"
            )
            subprocess.run(["git", "add", "docs/architecture.md"], cwd=root, check=True)
            res = self._run(root, "--private", "--strict")
            self.assertEqual(res.returncode, 1)
            self.assertIn("list item runs", res.stdout)

    def test_commented_gitignore_pattern_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            self._init_repo(root)
            gi = root / ".gitignore"
            lines = [
                f"# {ln}" if ln.strip() == "docs/acceptance-policy.md" else ln
                for ln in gi.read_text(encoding="utf-8").splitlines()
            ]
            gi.write_text("\n".join(lines) + "\n", encoding="utf-8")
            res = self._run(root, "--private")
            self.assertEqual(res.returncode, 1)
            self.assertIn("docs/acceptance-policy.md", res.stdout)


if __name__ == "__main__":
    unittest.main()
