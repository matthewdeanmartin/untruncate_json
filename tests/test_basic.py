import json

from half_json.core import JSONFixer
from hypothesis import given, strategies

from untruncate_json import complete

# from truncjson import truncjson


def test_array_one():
    assert complete("[1") == "[1]"


def test_array_two():
    assert complete("[1, 2") == "[1, 2]"


SAMPLE = json.dumps(
    {
        "name": "John",
        "age": 30,
        "city": "New York",
        "pets": [
            {"name": "Puffy", "type": "cat"},
            {"name": "Duffy", "type": "dog"},
        ],
    }
)


@given(strategies.integers(min_value=10, max_value=len(SAMPLE)))
def test_untruncate_various(length):
    # Can't assert because it sometimes returns valid falsy values.
    try:
        _ = json.loads(complete(SAMPLE[:length]))
    except json.JSONDecodeError:
        print("----")
        print(f"INPUT: {SAMPLE[:length]}")
        print(f"OUTPUT: {complete(SAMPLE[:length])}")
        raise


# @given(strategies.integers(min_value=10, max_value=len(SAMPLE)))
# def test_truncjson_various(length):
#     try:
#         json.loads(truncjson.complete(SAMPLE[:length]))
#     except json.JSONDecodeError:
#         print("----")
#         print(f"INPUT: {SAMPLE[:length]}")
#         print(f"OUTPUT: {truncjson.complete(SAMPLE[:length])}")
#         raise


# Failing Case:
# reported: https://github.com/half-pie/half-json/issues/15
# INPUT: {"name": "John", "age": 30,
# OUTPUT: {"name": "John", "age": 30,}
# @given(strategies.integers(min_value=10, max_value=len(SAMPLE)))
# def test_jsonfixer_various(length):
#     try:
#         json.loads(JSONFixer().fix(SAMPLE[:length]).line)
#     except json.JSONDecodeError:
#         print("----")
#         print(f"INPUT: {SAMPLE[:length]}")
#         print(f"OUTPUT: {JSONFixer().fix(SAMPLE[:length]).line}")
#         raise


def test_string():
    assert complete('"Hello, Wor') == '"Hello, Wor"'


def test_object():
    assert complete('{"votes": [true, fa') == '{"votes": [true, false]}'


def test_number():
    assert complete("123.") == "123.0"
