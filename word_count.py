"""Count whitespace-separated words in text."""

import argparse
from pathlib import Path
import sys


def count_words(text: str) -> int:
    """Return the number of whitespace-separated tokens in text."""
    return len(text.split())


def main() -> None:
    """Read text, a UTF-8 file, or stdin and print its word count."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version="word-count 1.0")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("text", nargs="?", help="text to count; quote text containing spaces")
    source.add_argument("--file", type=Path, help="UTF-8 file to count")
    source.add_argument("--stdin", action="store_true", help="read text from stdin")
    args = parser.parse_args()
    text = args.text
    if args.stdin:
        try:
            text = sys.stdin.read()
        except (OSError, UnicodeError) as error:
            parser.error(f"cannot read stdin: {error}")
    if args.file is not None:
        try:
            text = args.file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            parser.error(f"cannot read {args.file}: {error}")
    print(count_words(text))


if __name__ == "__main__":
    main()
