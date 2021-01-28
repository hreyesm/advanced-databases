file_name = "./data/soc-pokec-profiles.csv"

with open(file_name, 'r') as fin:
    data = fin.read().splitlines(True)

with open('soc-pokec-profiles1.csv', 'w') as fout1:
    fout1.writelines(data[:10000])