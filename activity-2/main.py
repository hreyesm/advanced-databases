from database import *
from bson import json_util
import json

db = Database()

def main():
    option = 1
    while option != -1: 
        option = int(input("\nSeleccione una query a ejecutar (1-5):\n\t1.Unwind\n\t2.Lookup\n\t3.GraphLookup\n\t4.GeoNear\n\t5.Facet\nIntroduzca -1 para salir\n"))
        if option == 1:
            query, result = db.unwind()
        elif option == 2:
            query, result = db.lookup()
        elif option == 3:
            query, result = db.graphLookup()
        elif option == 4:
            query, result = db.geoNear()
        elif option == 5:
            query, result = db.facet()
        if option != -1:
            print_results(query, result)

def print_results(query, result):
    print("------- QUERY -------\n", json.dumps(query, indent = 1, default=json_util.default))
    print("\n------ RESULTADOS ------\n", json.dumps(result, indent = 1))

if __name__ == "__main__":
    main()