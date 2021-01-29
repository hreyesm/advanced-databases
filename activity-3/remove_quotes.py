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

file_name = "./data/soc-pokec-profiles.txt"

data = ""

# Quitar comas y comillas
with open(file_name) as file:
     data = file.read().replace('"', "").replace(",","")

# Sobreescribir archivo con formato correcto
with open('./data/soc-pokec-profiles.txt', 'w') as new_file:
     new_file.write(data)
