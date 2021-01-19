import json
import random

curr_file = "users.json"

a_file = open(curr_file, "r")
json_object = json.load(a_file)
a_file.close()

#operation
for element in json_object:
    element['friends'] = [json_object[random.randint(0,99999)]['name'],json_object[random.randint(0,99999)]['name'], json_object[random.randint(0,99999)]['name'], json_object[random.randint(0,99999)]['name']]

a_file = open(curr_file, "w")
json.dump(json_object, a_file)
a_file.close()