import json


x = {}
x["name"] = 'x'
x['num'] = 1

print(x, type(x), json.dumps(x, indent=2))
