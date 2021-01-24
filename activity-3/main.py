"""
    Actividad 3: Bases de datos de grafos
    -----------------------------------------
    Curso: Bases de datos avanzadas
    Profesor: Vicente Cubells Nonell
    Equipo 5:
        Daniela Vignau León (A01021698)
        Cristopher Alan Cejudo Machuca (A01025468)
        Héctor Alexis Reyes Manrique (A01339607)
"""

from database import Database

def main():
    db = Database()
    option = 1
    while option != -1:
        try:
            option = int(input("\nSeleccione una consulta a ejecutar (1-3):\n\t1.----\n\t2.----\n\t3.----\nIntroduzca -1 para salir\n"))
            if option == 1:
                query = "\tMATCH (n:Movie)\n\tRETURN count(n)\n"
            elif option == 2:
                query = "\tMATCH (n:Movie)\n\tRETURN count(n)\n"
            elif option == 3:
                query = "\tMATCH (n:Movie)\n\tRETURN count(n)\n"
            if option != -1:
                res = db.run(query)  
                print_response(query, res)
                db.close()
        except:
            print("Hubo un problema. Por favor seleccione una opción válida")

def print_response(query, result):
    print("\nQuery:\n", query)
    print("Response:\n\t", result)

if __name__ == "__main__":
    main()