"""Run outside the checkout to ensure wheel tests exercise compiled code."""
from importlib.machinery import EXTENSION_SUFFIXES
import untruncate_json.untrunc as parser

assert any(parser.__file__.endswith(suffix) for suffix in EXTENSION_SUFFIXES), parser.__file__
assert parser.complete('[1') == '[1]'
