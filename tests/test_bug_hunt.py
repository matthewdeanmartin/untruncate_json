"""Exercise complete documents and every truncation boundary."""

import json
import subprocess
import sys
from typing import Optional

import pytest
from hypothesis import given, settings, strategies as st

from untruncate_json import complete


VALUES = st.recursive(
    st.none() | st.booleans() | st.integers()
    | st.floats(allow_nan=False, allow_infinity=False) | st.text(max_size=20),
    lambda child: st.lists(child, max_size=3)
    | st.dictionaries(st.text(max_size=10), child, max_size=3),
    max_leaves=10,
)


@settings(max_examples=500, deadline=None)
@given(VALUES, st.booleans(), st.sampled_from([None, 2]))
def test_every_truncation_boundary(value: object, ensure_ascii: bool, indent: Optional[int]) -> None:
    text = json.dumps(value, ensure_ascii=ensure_ascii, indent=indent, allow_nan=False)
    assert complete(text) == text
    for end in range(1, len(text) + 1):
        repaired = complete(text[:end])
        json.loads(repaired)
        assert complete(repaired) == repaired


@pytest.mark.parametrize(
    ("text", "expected"),
    [('{"items":[1,', '{"items":[1]}\n'), ('"hello', '"hello"\n'), ('true', 'true\n')],
)
def test_python_module_cli(text: str, expected: str) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "untruncate_json"],
        input=text, capture_output=True, text=True, check=True,
    )
    assert result.stdout == expected
    assert result.stderr == ""
