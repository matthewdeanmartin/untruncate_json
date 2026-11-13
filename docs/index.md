# untruncate_json

Repair a JSON document cut off at the end, such as an interrupted API response.
The library returns a string you can parse with Python's `json` module.

```python
import json
from untruncate_json import complete

repaired = complete('{"items": [1, 2,')
assert json.loads(repaired) == {"items": [1, 2]}
```

## Install

```sh
pip install untruncate_json
```

The package supports standard CPython 3.9–3.15. Release automation builds native
mypyc wheels for Windows x64, macOS Intel and Apple Silicon, and Linux x64 and
ARM64 (manylinux and musllinux). Free-threaded Python and PyPy are not targeted.
Installing from source requires a C compiler; runtime dependencies are empty.

Start with [Usage and API](usage.md), or see [Development](development.md) and
[Releases](releases.md) for contributor instructions.

## Scope

This is a truncation repair tool, not a general JSON validator or a way to recover
lost values. It may discard unfinished object keys, trailing commas, and incomplete
string escapes. Review repaired data before relying on its meaning.

The implementation was translated from
[dphilipson/untruncate-json](https://github.com/dphilipson/untruncate-json).
It is distributed under the MIT license.
