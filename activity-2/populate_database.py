import json
import os
import pymongo
import datetime
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("mongo_url")

client = pymongo.MongoClient(url)
db = client.actividad2

with open('users.json') as u:
    users_data = json.load(u)

with open('posts.json') as p:
    posts_data = json.load(p)

with open('hashtags.json') as h:
    hashtags_data = json.load(h)

collection_users = db['users']
collection_posts = db['posts']
collection_hashtags = db['hashtags']

for element in posts_data:
    element['date'] = datetime.datetime.strptime(element['date'], "%Y-%m-%dT%H:%M:%S%fZ")

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

try:
    collection_posts.create_index([('coordinates', pymongo.GEO2D)])
    print('2D Sphere index created')
except:
    print('something happened while creating index')

client.close()
