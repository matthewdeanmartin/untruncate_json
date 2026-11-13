"""Compile the parser; project metadata lives in pyproject.toml."""
import os

from setuptools import setup
from mypyc.build import mypycify

setup(
    ext_modules=mypycify(
        ["untruncate_json/untrunc.py"],
        opt_level=os.environ.get("MYPYC_OPT_LEVEL", "3"),
        debug_level="0",
    ),
)
