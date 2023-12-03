# import jsonfixer
import truncjson
from half_json.core import JSONFixer

import untruncate_json

print(untruncate_json.complete("[1"))
print(truncjson.complete("[1"))

result = JSONFixer().fix("[1")
print(result.line)
