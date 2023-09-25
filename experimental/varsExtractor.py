from constants import constants
import re
import json

count = 0
my_dict = {}
attrs = constants.split(";\n")
for attr in attrs:
    if attr == "":
        continue
    temp = re.sub(r'false', 'False', re.sub(r'null', 'None', re.sub(r'"', "", re.sub(r'\s+', " ", attr)))).strip().split(" ")
    # print(f"{temp} - {count + 1}")
    attr = re.sub(r'false', 'False', re.sub(r'null', 'None', re.sub(r'"', "", re.sub(r'\s+', " ", attr)))).strip().split(" ")[-3:]
    print(f"{attr} - {count + 1}")
    if len(attr) < 3 or attr[1] != "=":
        continue
    count += 1
    my_dict.__setitem__(attr[0], attr[2])

with open("./experimental/my_dict.json", "w") as f:
    json.dump(my_dict, f, indent=4)
print(count)

# count = 0
# attrs = constants.split(";\n")
# for attr in attrs:
#     if attr == "":
#         continue
#     count += 1
#     print(f"{count}, {attr}")