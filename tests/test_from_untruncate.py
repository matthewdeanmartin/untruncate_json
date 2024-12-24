"""
Credit:
https://github.com/dphilipson/untruncate-json/blob/master/src/index.ts
License: MIT
"""

import json

import pytest

from untruncate_json import complete


def expect_unchanged(json_str):
    assert complete(json_str) == json_str


def test_returns_unmodified_valid_string():
    expect_unchanged('"Hello"')


def test_returns_unmodified_valid_string_with_bracket_characters():
    expect_unchanged('"}{]["')


def test_returns_unmodified_valid_string_with_escaped_quotes():
    expect_unchanged('"\\"Dr.\\" Leo Spaceman"')


def test_returns_unmodified_valid_string_with_unicode_escapes():
    expect_unchanged("ab\\u0065cd")


def test_returns_unmodified_valid_number():
    expect_unchanged("20")


def test_returns_unmodified_valid_boolean():
    expect_unchanged("true")
    expect_unchanged("false")


def test_returns_unmodified_valid_null():
    expect_unchanged("null")


def test_returns_unmodified_valid_array():
    expect_unchanged("[]")
    expect_unchanged('["a", "b", "c"]')
    expect_unchanged("[ 1, 2, 3 ]")


def test_returns_unmodified_valid_object():
    expect_unchanged("{}")
    expect_unchanged('{"foo": "bar"}')
    expect_unchanged('{ "foo": 2 }')


def test_returns_unmodified_compound_object():
    expect_unchanged(
        '{"s": "Hello", "num": 10, "b": true, "nul": "null", "o": { "s": "Hello2", "num": 11 }, "a": ["Hello", 10, { "s": "Hello3" }]}'
    )


def test_adds_missing_close_quote():
    assert complete('"Hello') == '"Hello"'


def test_cut_off_trailing_backslash():
    assert complete('"Hello\\') == '"Hello"'


def test_cut_off_partial_unicode_escape():
    assert complete('"ab\\u006') == '"ab"'


def test_adds_zero_to_number_cut_off_at_a_negative_sign():
    assert complete("-") == "-0"


def test_adds_zero_to_number_cut_off_at_a_decimal_point():
    assert complete("12.") == "12.0"


def test_adds_zero_to_number_cut_off_at_an_exponent():
    assert complete("12e") == "12e0"
    assert complete("12E") == "12E0"


def test_add_zero_to_number_cut_off_after_e():
    assert complete("12e+") == "12e+0"
    assert complete("12E-") == "12E-0"


def test_completes_boolean_and_null_literals():
    assert complete("tr") == "true"
    assert complete("fal") == "false"
    assert complete("nu") == "null"


def test_close_empty_array():
    assert complete("[") == "[]"


def test_close_array_with_items():
    assert complete('["a", "b"') == '["a", "b"]'


def test_close_a_list_ending_in_a_number():
    assert complete("[1, 2") == "[1, 2]"


def test_completes_boolean_and_null_literals_at_the_end_of_a_list():
    assert complete("[tr") == "[true]"
    assert complete("[true, fa") == "[true, false]"
    assert complete("[nul") == "[null]"


def test_removes_a_trailing_comma_to_end_a_list():
    assert complete("[1, 2,") == "[1, 2]"


def test_closes_an_empty_object():
    assert complete("{") == "{}"


def test_closes_an_object_after_key_value_pairs():
    assert complete('{"a": "b"') == '{"a": "b"}'
    assert complete('{"a": 1') == '{"a": 1}'


def test_custs_off_a_partial_key_in_an_object():
    assert complete('{"hel') == "{}"
    assert complete('{"hello": 1, "wo') == '{"hello": 1}'


def test_cuts_off_a_key_missing_a_colon_in_an_object():
    assert complete('{"hello') == "{}"
    assert complete('{"hello": 1, "world') == '{"hello": 1}'


def test_cuts_off_a_key_and_colon_without_a_value_in_an_object():
    assert complete('{"hello":') == "{}"
    assert complete('{"hello": 1, "world": ') == '{"hello": 1}'


def test_untruncates_a_value_in_an_object():
    assert complete('{"hello": "wo') == '{"hello": "wo"}'
    assert complete('{"hello": [1, 2') == '{"hello": [1, 2]}'


def test_handles_a_string_in_an_array_cut_off_at_a_backslash():
    assert complete('["hello\\') == '["hello"]'
    assert complete('["hello", "world\\') == '["hello", "world"]'


def test_handles_a_cut_off_string_in_an_array_with_an_escaped_character():
    assert complete('["hello", "\\"Dr.]\\" Leo Spaceman') == '["hello", "\\"Dr.]\\" Leo Spaceman"]'


def test_handles_a_string_in_an_object_key_cut_off_at_a_backslash():
    assert complete('{"hello\\') == "{}"
    assert complete('{"hello": 1, "world\\') == '{"hello": 1}'


def test_removes_cut_off_object_with_key_containing_escaped_characters():
    assert complete('{"hello\\nworld": ') == "{}"
    assert complete('{"hello": 1, "hello\\nworld') == '{"hello": 1}'


def test_should_produce_valid_json_wherever_truncation_occurs():
    json_str = """{
        "ab\\nc\\u0065d": ["ab\\nc\\u0065d", true, false, null, -12.3e-4],
        "": { "12": "ab\\nc\\u0065d"}
    }"""
    for i in range(1, len(json_str)):
        partial_json = json_str[:i]
        fixed_json = complete(partial_json)
        try:
            json.loads(fixed_json)
        except json.JSONDecodeError:
            pytest.fail(
                f"Failed to produce valid JSON.\n\nInput:\n\n{partial_json}\n\nOutput (invalid JSON):\n\n{fixed_json}\n"
            )
