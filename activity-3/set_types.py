"""
    Actividad 3: Bases de datos de grafos
    -------------------------------------
    Curso: Bases de datos avanzadas
    Profesor: Vicente Cubells Nonell
    Equipo 5:
        Daniela Vignau León (A01021698)
        Cristopher Alan Cejudo Machuca (A01025468)
        Héctor Alexis Reyes Manrique (A01339607)
"""

file_name = "./data/soc-pokec-relationships.csv"

with open(file_name, 'r') as fin:
    data = fin.read().splitlines(True)

#Primeros 10M de registros
with open('soc-pokec-relationships1.csv', 'w') as fout1:
    fout1.writelines(data[:10000000])

#Segundos 10M de registros
with open('soc-pokec-relationships2.csv', 'w') as fout2:
    fout2.writelines(data[0]) #Headers
    fout2.writelines(data[10000000:20000000])

#Registros Restantes
with open('soc-pokec-relationships3.csv', 'w') as fout3:
    fout3.writelines(data[0]) #Headers
    fout3.writelines(data[:20000000])
