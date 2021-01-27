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

from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()
url = os.getenv("neo4j_url")
# user = os.getenv("user")
# pwd = os.getenv("pwd")

class Database:
    def __init__(self):
        # self.driver = GraphDatabase.driver(url, auth=(user, pwd))
        self.driver = GraphDatabase.driver(url)
        
    def close(self):
        self.driver.close()
        
    def run(self, query):
        db = 'neo4j'
        session = self.driver.session(database=db) 
        response = list(session.run(query))
        session.close()
        return response