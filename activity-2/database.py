"""
    Actividad 2: Bases de datos de documentos
    -----------------------------------------
    Curso: Bases de datos avanzadas
    Profesor: Vicente Cubells Nonell
    Equipo 5:
        Daniela Vignau León (A01021698)
        Cristopher Alan Cejudo Machuca (A01025468)
        Héctor Alexis Reyes Manrique (A01339607)
"""

from datetime import datetime, tzinfo, timezone
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
url = os.getenv("mongo_url")


class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(url)
        self.db = self.client.actividad2

    def unwind(self):
        """
        Obtener, en orden descendente, la cantidad de personas de nombre "Murphy" que están inscritas por grupo.
        Etapas: 
            - match: Filtra los documentos por el nombre "Murphy"
            - unwind: Descompone los documentos obtenidos bajo el criterio "groups"
            - group: Cuenta el número de personas con el nombre "Murphy" que pertecen a cada uno de los grupos
            - sort: Ordena los resultados de manera descendente
        """
        query = [
            {"$match": {"name": "Murphy"}},
            {"$unwind": {"path": "$groups"}},
            {"$group": {"_id": "$groups", "enrolled": {"$sum": 1}}},
            {"$sort": {"enrolled": -1}},
        ]
        users = self.db["users"]
        unwind = users.aggregate(query)
        self.client.close()
        return query, list(unwind)

    def lookup(self):
        """
        Obtener el promedio de likes de los 10 posts con más likes asociados con el hashtag "semper".
        Etapas:
            - lookup: Produce la unión de las colecciones "posts" y "hashtags"
            - replaceRoot: Extrae el contenido del atributo "hashtagInfo" y lo coloca al mismo nivel de los atributos exteriores
            - match: Filtra los documentos por el nombre "semper"
            - sort: Ordena los documentos de mayor a menor número de likes
            - limit: Limita los resultados a 10
            - group: Obtiene el promedio de likes
            - project: Muestra únicamente el atributo "averageLikes"
        """
        query = [
            {
                "$lookup": {
                    "from": "hashtags",
                    "localField": "hashtag",
                    "foreignField": "_id",
                    "as": "hashtagInfo",
                }
            },
            {
                "$replaceRoot": {
                    "newRoot": {
                        "$mergeObjects": [
                            {"$arrayElemAt": ["$hashtagInfo", 0]},
                            "$$ROOT",
                        ]
                    }
                }
            },
            {"$match": {"name": "semper"}},
            {"$sort": {"likes": -1}},
            {"$limit": 10},
            {"$group": {"_id": "$name", "averageLikes": {"$avg": "$likes"}}},
            {"$project": {"_id": 0, "averageLikes": 1}},
        ]
        posts = self.db["posts"]
        lookup = posts.aggregate(query)
        self.client.close()
        return query, list(lookup)

    def graph_lookup(self):
        """
        Obtener el número total de likes de los posts cuyo autor sea amigo mutuo del usuario con email "quis.diam.luctus@ultricies.net" con mayor número de likes acumulados entre sus posts.
        Etapas:
            - match: Filtra los documentos a partir del correo electrónico "quis.diam.luctus@ultricies.net"
            - graphLookup: Recopila los amigos del dueño del correo electrónico especificado que pertenecen al grupo ITC y que, además, tienen como amigo al dueño del correo electrónico ("Marah")
            - project: Obtiene el ID de los amigos anteriormente encontrados
            - unwind: Descompone los documentos bajo el criterio "connections"
            - lookup: Realiza la unión de las colecciones "users" y "posts"
            - sort: Ordena de manera descencente los resultados obtenidos
            - limit: Limita los resultados a 1 para obtener el documento con mayor número de likes
            - unwind: Descompone el documento a partir del criterio "postInfo"
            - group: Realiza la suma total de likes
            - project: Muestra únicamente la suma
        """
        query = [
            {"$match": {"email": "quis.diam.luctus@ultricies.net"}},
            {
                "$graphLookup": {
                    "from": "users",
                    "startWith": "$friends",
                    "connectFromField": "friends",
                    "connectToField": "name",
                    "as": "ITCs",
                    "maxDepth": 2,
                    "restrictSearchWithMatch": {"groups": "ITC", "friends": "Marah"},
                }
            },
            {"$project": {"connections": "$ITCs._id"}},
            {"$unwind": {"path": "$connections"}},
            {
                "$lookup": {
                    "from": "posts",
                    "localField": "connections",
                    "foreignField": "user",
                    "as": "postInfo",
                }
            },
            {"$sort": {"postInfo.likes": -1}},
            {"$limit": 1},
            {"$unwind": {"path": "$postInfo"}},
            {"$group": {"_id": None, "totalLikes": {"$sum": "$postInfo.likes"}}},
            {"$project": {"_id": 0}},
        ]
        users = self.db["users"]
        graph_lookup = users.aggregate(query)
        self.client.close()
        return query, list(graph_lookup)

    def geo_near(self):
        """
        Obtener la distancia promedio que existe a partir de la coordenada [-77.73, -5.71] tomando como referencia los 56 posts con mayor distancia del punto original cuya fecha de publicación está entre '2021-01-01' y '2020-06-01' y que tienen más de 950 likes.
        Etapas:
            - geoNear: Encuentra la distancia que existe a partir del punto [-77.73, -5.71] con el resto de los documentos en la colección "posts"
            - match: Filtra los documentos por fecha de publicación (2021-01-01 y 2020-06-01) y por aquellos que tengan más de 950 likes
            - sort: Ordena los documentos de manera ascendente
            - skip: En este momento, existen 106 documentos, por lo que se descartan los primeros 50 y se conservan los 56 restantes
            - group: Computar la distancia promedio en los 50 posts restantes
            - project: Mostrar únicamente la distancia obtenida
        """
        query = [
            {
                "$geoNear": {
                    "near": {"type": "Point", "coordinates": [-77.73, -5.71]},
                    "distanceField": "distance",
                }
            },
            {
                "$match": {
                    "date": {
                        "$lt": datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "$gte": datetime(2020, 6, 1, 0, 0, 0, tzinfo=timezone.utc),
                    },
                    "likes": {"$gt": 950},
                }
            },
            {"$sort": {"distance": 1}},
            {"$skip": 50},
            {"$group": {"_id": "distance", "averageDistance": {"$avg": "$distance"}}},
            {"$project": {"_id": 0, "averageDistance": 1}},
        ]
        posts = self.db["posts"]
        geo_near = posts.aggregate(query)
        self.client.close()
        return query, list(geo_near)

    def facet(self):
        print("PENDING")
