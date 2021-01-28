file_name = "./data/soc-pokec-profiles.txt"

data = ""

with open(file_name) as file:
     data = file.read().replace('"', "").replace(",","")
     # data = file.read().splitlines(True)

with open('./data/new-soc-pokec-profiles.txt', 'w') as new_file:
     new_file.write(data)