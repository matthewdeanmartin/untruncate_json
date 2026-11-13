# Usage and API

## `complete(json_str: str) -> str`

Import the public function from `untruncate_json`. Pass a string containing a
complete JSON document or a prefix of one. The return value is a string, not a
Python dictionary or list. Complete valid JSON is preserved.

```python
import json
from untruncate_json import complete

assert complete('{"foo": "bar') == '{"foo": "bar"}'
assert complete('[true, fa') == '[true, false]'
assert complete('123.') == '123.0'
assert complete('{"done": 1, "unfinished":') == '{"done": 1}'
assert json.loads(complete('[1, 2,')) == [1, 2]
```

Repairs close strings and containers, complete partial `true`, `false`, and
`null` literals, and add zero where a number needs a digit. Incomplete Unicode
escapes and trailing backslashes in strings are discarded.

Empty or whitespace-only input is returned unchanged; no value is invented.
Arbitrary malformed JSON is outside the supported contract. If you need a Python
value, call `json.loads` on the result and handle `json.JSONDecodeError`.

## Command line

Both entry points read all of standard input and print the repaired text followed
by a newline:

```sh
printf '%s' '{"items": [1, 2,' | untruncate_json
printf '%s' '{"items": [1, 2,' | python -m untruncate_json
```

Output:

```json
{"items": [1, 2]}
```

The CLI accepts input through stdin, not a filename argument. It reads the whole
input into memory; it is not a streaming parser.
