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

from database import Database

def main():
    db = Database()
    option = 1
    while option != -1:
        try:
            option = int(input("\nSeleccione una consulta a ejecutar (1-3):\n\t1.Obtener el número de amigos que tienen en común dos personas\n\t2.Obtener el userID, género y edad de las personas que trabajan en la misma área y que se encuentran a una distancia de 2 a 3 nodos de distancia.\n\t3.Obtener el numero de personas que tienen una relación de amistad mútua, que tienen un perfil público y que tengan la misma edad\nIntroduzca -1 para salir\n"))
            if option == 1:
                query = "\tMATCH (p1:Profile {userID: '16'})\n\tMATCH (p2:Profile {userID: '2'})\n\tRETURN gds.alpha.linkprediction.commonNeighbors(p1, p2) AS Friends_In_Common\n"
            elif option == 2:
                query = "\tMATCH (p:Profile {userID: '1'})-[*2..3]->(q:Profile)\n\tWHERE p.I_am_working_in_field = q.I_am_working_in_field\n\tRETURN q.userID, q.gender, q.AGE\n"                
            elif option == 3:
                query = "\tMATCH (n:Profile)-[:FRIENDS_WITH]->(m:Profile), (n)<-[:FRIENDS_WITH]-(m)\n\tWHERE n.public = '1' and n.AGE = m.AGE and toInteger(n.userID) < 10\n\tRETURN COUNT (*)\n"
            if option != -1:
                res = db.run(query)  
                print_response(query, res)
                db.close()
        except:
            print("Hubo un problema. Por favor seleccione una opción válida")

def print_response(query, res):
    print("\nQuery:\n", query)
    print("Response:\n\t", res)


if __name__ == "__main__":
    main()