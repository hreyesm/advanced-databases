file_name = "./data/soc-pokec-relationships.csv"

with open(file_name, 'r') as fin:
    data = fin.read().splitlines(False)

for i in range(1, len(data)):
    data[i] = data[i]+',FRIENDS_WITH\n'

with open(file_name + 'new', 'w') as fout:
    fout.writelines(data[1:])