"""Tests for the word-count function and command-line interface."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from word_count import count_words, main


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "word_count.py"


class CountWordsTests(unittest.TestCase):
    def test_counts_whitespace_separated_tokens(self):
        cases = [
            ("", 0),
            (" \t\n ", 0),
            ("hello agent team", 3),
            ("  hello\tagent\nteam  ", 3),
            ("hello, world! isn't punctuation-separated", 4),
            ("բարև աշխարհ こんにちは 世界", 4),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(count_words(text), expected)


class CommandLineTests(unittest.TestCase):
    def assert_cli_error(self, result):
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def run_cli(self, *args, input=None):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *args],
            capture_output=True,
            text=True,
            input=input,
            check=False,
            timeout=5,
        )

    def test_prints_count(self):
        result = self.run_cli("hello agent team")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "3\n")
        self.assertEqual(result.stderr, "")

    def test_accepts_empty_text(self):
        result = self.run_cli("")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "0\n")
        self.assertEqual(result.stderr, "")

    def test_requires_text_argument(self):
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("usage:", result.stderr)

    def test_counts_stdin(self):
        for content, expected in [
            ("", 0),
            (" \t\n ", 0),
            ("hello agent\nteam\n", 3),
            ("բարև աշխարհ\nこんにちは 世界", 4),
        ]:
            with self.subTest(content=content):
                result = self.run_cli("--stdin", input=content)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, f"{expected}\n")
                self.assertEqual(result.stderr, "")

    def test_piped_input_requires_explicit_source(self):
        result = self.run_cli(input="hello agent team")
        self.assert_cli_error(result)
        self.assertEqual(result.returncode, 2)

    def test_counts_utf8_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample text.txt"
            for content, expected in [("բարև աշխարհ\nhello\tteam", 4), ("", 0), (" \t\n", 0)]:
                with self.subTest(content=content):
                    path.write_text(content, encoding="utf-8")
                    result = self.run_cli("--file", str(path))
                    self.assertEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, f"{expected}\n")
                    self.assertEqual(result.stderr, "")

    def test_rejects_conflicting_or_missing_inputs(self):
        for args in [(), ("--file",), ("text", "--file", "sample.txt"), ("", "--file", "sample.txt")]:
            with self.subTest(args=args):
                self.assert_cli_error(self.run_cli(*args))

    def test_conflicting_sources_do_not_read_stdin(self):
        conflicts = [
            ("text", "--file", "sample.txt"),
            ("", "--file", "sample.txt"),
            ("text", "--stdin"),
            ("", "--stdin"),
            ("--file", "sample.txt", "--stdin"),
            ("text", "--file", "sample.txt", "--stdin"),
            ("", "--file", "sample.txt", "--stdin"),
        ]
        for args in conflicts:
            with self.subTest(args=args):
                result = self.run_cli(*args, input="ignored input")
                self.assert_cli_error(result)
                self.assertEqual(result.returncode, 2)
                with (
                    patch.object(sys, "argv", [str(SCRIPT), *args]),
                    patch("word_count.sys.stdin") as stdin,
                    patch("sys.stdout") as stdout,
                    patch("sys.stderr"),
                ):
                    with self.assertRaises(SystemExit) as error:
                        main()
                    self.assertEqual(error.exception.code, 2)
                    stdin.read.assert_not_called()
                    stdout.write.assert_not_called()

    def test_reports_file_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = root / "invalid.txt"
            invalid.write_bytes(b"\xff")
            for path in [root / "missing.txt", root, invalid]:
                with self.subTest(path=path):
                    result = self.run_cli("--file", str(path))
                    self.assert_cli_error(result)
                    self.assertIn("cannot read", result.stderr)

    def test_import_has_no_cli_side_effects(self):
        result = subprocess.run(
            [sys.executable, "-B", "-c", "import word_count"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
