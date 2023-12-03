# untruncate_json
Python library to repair truncated json. Translated directly from the typescript original version

## Installation

```bash
pip install untruncate_json
```
## Usage

In some cases, a partial json document is invalid and there is no way to recover. A common scenario using OpenAI's chatbot is that the AI created json is truncated at the end of the document. This library will attempt to repair the json by adding the missing closing brackets.

If the context of the json is relatively simple and holds natural language, truncating the text might not degrade the final result much.

```python
import untruncate_json
assert untruncate_json.complete('{"foo": "bar') == '{"foo": "bar"}'
```

## Goals
My goal is for the library to be a pure python library that handles as many cases as the other libraries.

## Credits
Original Typescript version by dphilipson, MIT license. Code translated by a lazy ChatGPT that didn't
want to translate the long switch blocks. Copilot translated the switch blocks.

## Prior Art

- [untruncate-json](https://github.com/dphilipson/untruncate-json) - Original Typescript version
- [truncjson](https://pypi.org/project/truncjson/) Cython implementation
- [jsonfixer](https://pypi.org/project/jsonfixer/) Fork of half-json?
- [half-json](https://pypi.org/project/halfjson/)

## Benchmarks

- truncjson: 1.28
- untruncate_json: 11.39
- untruncate_json: 1.14 (if you run `mypyc untruncate_json`
- jsonfixer: 23.06


