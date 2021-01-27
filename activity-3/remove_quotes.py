file_name = "./data/soc-pokec-profiles.csv"

data = ""

with open(file_name) as file:
     data = file.read().replace('"', '$')
     # data = file.read().splitlines(True)

with open('./data/new-soc-pokec-profiles.csv', 'w') as new_file:
     new_file.write(data)