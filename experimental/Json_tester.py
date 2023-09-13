import json

x = {}
x["name"] = 'x'
x['num'] = 1

print(x, type(x), json.dumps(x, indent=2))

try:
    raise IOError("--------")
except Exception :
    print("handled")


def add_1(x):
    x += 10


x = [1]
print(x)
add_1(x[0])
print(x)
