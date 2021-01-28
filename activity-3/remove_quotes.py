file_name = "./data/soc-pokec-profiles.txt"

data = ""

#Quitar comas y comillas
with open(file_name) as file:
     data = file.read().replace('"', "").replace(",","")

#Nuevo archivo con formato correcto
with open('./data/new-soc-pokec-profiles.txt', 'w') as new_file:
     new_file.write(data)