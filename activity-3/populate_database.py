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
    # _ = db.run('USING PERIODIC COMMIT\nLOAD CSV WITH HEADERS FROM "file:///pokec/pokec-fixed.csv" AS row\nCREATE (:Node {nodeID: row.user_id});')

    _ = db.run('CREATE INDEX FOR (n:Node) ON (n.nodeID);')
    
    _ = db.run(':auto USING PERIODIC COMMIT\nLOAD CSV WITH HEADERS FROM "file:///pokec/soc-pokec-relationships.csv" AS row\nMATCH (start:Node {nodeID: row.start_id})\nMATCH (end:Node {nodeID: row.end_id})\nMERGE (start)-[:FRIENDS_WITH]->(end);')

    db.close()

if __name__ == '__main__':
    main()