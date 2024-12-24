import json
import timeit

# import truncjson
from half_json.core import JSONFixer

import untruncate_json

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

def speed_untruncate_json():
    for i in range(len(SAMPLE)):
        untruncate_json.complete(SAMPLE[:i])

# def speed_truncjson():
#     for i in range(len(SAMPLE)):
#         truncjson.complete(SAMPLE[:i])

SINGLETON = JSONFixer()
def speed_jsonfixer():
    for i in range(len(SAMPLE)):
        SINGLETON.fix(SAMPLE[:i])

time_jsonfixer = timeit.timeit(speed_jsonfixer, number=1000)
print(f"jsonfixer: {time_jsonfixer}")
# time_truncjson = timeit.timeit(speed_truncjson, number=1000)
# print(f"truncjson: {time_truncjson}")
time_untruncate_json = timeit.timeit(speed_untruncate_json, number=1000)
print(f"untruncate_json: {time_untruncate_json}")