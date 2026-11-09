"""Count whitespace-separated words in text."""

import argparse


def count_words(text: str) -> int:
    """Return the number of whitespace-separated tokens in text."""
    return len(text.split())


def main() -> None:
    """Parse one text argument and print its word count."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", help="text to count; quote text containing spaces")
    args = parser.parse_args()
    print(count_words(args.text))


if __name__ == "__main__":
    main()
