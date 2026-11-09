"""Tests for the word-count function and command-line interface."""

from pathlib import Path
import subprocess
import sys
import unittest

from word_count import count_words


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
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
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

    def test_import_has_no_cli_side_effects(self):
        result = subprocess.run(
            [sys.executable, "-c", "import word_count"],
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
