"""
    Actividad 2: Bases de datos de documentos
    -----------------------------------------
    Curso: Bases de datos avanzadas
    Profesor: Vicente Cubells Nonell
    Equipo 5
    Integrantes:
        Cristopher Alan Cejudo Machuca (A01025468)
        Daniela Vignau León (A01021698)
        Héctor Alexis Reyes Manrique (A01339607)
"""

from bson import json_util
from database import Database
import json

db = Database()


def main():
    option = 1
    while option != -1:
        try:
            option = int(
                input(
                    "\nSeleccione una query a ejecutar (1-5):\n\t1. unwind\n\t2. lookup\n\t3. graphLookup\n\t4. geoNear\n\t5. facet\nIntroduzca -1 para salir\n"
                )
            )
            if option == 1:
                query, result = db.unwind()
            elif option == 2:
                query, result = db.lookup()
            elif option == 3:
                query, result = db.graph_lookup()
            elif option == 4:
                query, result = db.geo_near()
            elif option == 5:
                query, result = db.facet()
            if option != -1:
                print_results(query, result)
        except:
            print("Por favor seleccione una opción válida")


def print_results(query, result):
    print(
        "------- QUERY -------\n",
        json.dumps(query, indent=1, default=json_util.default),
    )
    print("\n------ RESULTADO ------\n", json.dumps(result, indent=1, default=str))


if __name__ == "__main__":
    main()
