"""
CLI interface
"""

import sys

from untruncate_json.untrunc import complete


def main() -> None:
    """Read string piped in and pass to complete function and then write result to console."""
    print(complete(sys.stdin.read()))
