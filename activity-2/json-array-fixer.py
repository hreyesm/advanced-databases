import json
import random

curr_file = "posts.json"

a_file = open(curr_file, "r")
json_object = json.load(a_file)
a_file.close()

#operation
for element in json_object:
    element['date'] = 'ISODate(' + element['date']['$date'] +')'

a_file = open(curr_file, "w")
json.dump(json_object, a_file)
a_file.close()