"""Count whitespace-separated words in text."""

import argparse
from pathlib import Path


def count_words(text: str) -> int:
    """Return the number of whitespace-separated tokens in text."""
    return len(text.split())


def main() -> None:
    """Read text or a UTF-8 file and print its word count."""
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("text", nargs="?", help="text to count; quote text containing spaces")
    source.add_argument("--file", type=Path, help="UTF-8 file to count")
    args = parser.parse_args()
    text = args.text
    if args.file is not None:
        try:
            text = args.file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            parser.error(f"cannot read {args.file}: {error}")
    print(count_words(text))


if __name__ == "__main__":
    main()
