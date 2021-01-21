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

import json
import os
import pymongo
import datetime
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("mongo_url")

#Conexión a Mongo
client = pymongo.MongoClient(url)
db = client.actividad2

#Carga de archivos json
with open('./data/users.json') as u:
    users_data = json.load(u)

with open('./data/posts.json') as p:
    posts_data = json.load(p)

with open('./data/hashtags.json') as h:
    hashtags_data = json.load(h)

#Collecciones creadas
collection_users = db['users']
collection_posts = db['posts']
collection_hashtags = db['hashtags']

#Ciclo para insertar fechas en formato correcto
for element in posts_data:
    element['date'] = datetime.datetime.strptime(element['date'], "%Y-%m-%dT%H:%M:%S%fZ")

#Inserción de datos
print('Starting database population. This may take a while...')
try:
    collection_users.insert_many(users_data)
    print('users succesfully added')
    collection_posts.insert_many(posts_data)
    print('posts succesfully added')
    collection_hashtags.insert_many(hashtags_data)
    print('hashtags succesfully added')
except:
    print('something happened while inserting documents')

print('Creating indexes...')

#Creación de index
try:
    collection_posts.create_index([('coordinates', pymongo.GEOSPHERE)])
    print('2D Sphere index created')
except:
    print('something happened while creating index')

#Fin de conexión
client.close()
