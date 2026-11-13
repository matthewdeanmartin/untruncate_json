"""Regression coverage for nested truncation, escaping, and the CLI."""

import io
import json

import pytest
from hypothesis import given, strategies as st

from untruncate_json import complete
from untruncate_json.__main__ import main


@pytest.mark.parametrize(
    ("partial", "expected"),
    [
        ('{"a":[{"b":', '{"a":[{}]}'),
        ('{"a":[1,2, \n', '{"a":[1,2]}'),
        ('[{"a":1,"b', '[{"a":1}]'),
        ('{"a":-12E+', '{"a":-12E+0}'),
        ('["a\\u12', '["a"]'),
        ('["a\\u1234', '["a\\u1234"]'),
        ('{"a":"x\\', '{"a":"x"}'),
        ('[[[', '[[[]]]'),
        ('[t', '[true]'),
        ('[f', '[false]'),
        ('[n', '[null]'),
    ],
)
def test_nested_truncation(partial: str, expected: str) -> None:
    assert complete(partial) == expected
    json.loads(expected)
    assert complete(expected) == expected


@pytest.mark.parametrize("text", ["", " ", "\r\n\t"])
def test_no_value_is_not_invented(text: str) -> None:
    assert complete(text) == text


JSON_VALUES = st.recursive(
    st.none() | st.booleans() | st.integers() | st.text(),
    lambda children: st.lists(children, max_size=4)
    | st.dictionaries(st.text(), children, max_size=4),
    max_leaves=12,
)


@given(JSON_VALUES)
def test_complete_json_is_preserved(value: object) -> None:
    text = json.dumps(value)
    assert complete(text) == text


@given(JSON_VALUES, st.data())
def test_truncated_json_is_valid_and_idempotent(value: object, data: st.DataObject) -> None:
    text = json.dumps(value)
    end = data.draw(st.integers(min_value=1, max_value=len(text)))
    repaired = complete(text[:end])
    json.loads(repaired)
    assert complete(repaired) == repaired


def test_deep_nesting_without_python_recursion() -> None:
    assert complete("[" * 1500) == "[" * 1500 + "]" * 1500


def test_cli_reads_all_input_and_prints_completed_json(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO('{\n"items": [1, 2,'))
    main()
    captured = capsys.readouterr()
    assert captured.out == '{\n"items": [1, 2]}\n'
    assert captured.err == ""
