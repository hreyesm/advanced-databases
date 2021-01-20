import os
import pymongo
from datetime import datetime, tzinfo, timezone
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("mongo_url")

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(url)
        self.db = self.client.actividad2
    
    def unwind(self):
        query = [
            {
                '$match': {
                    'name': 'Murphy'
                }
            }, {
                '$unwind': {
                    'path': '$groups'
                }
            }, {
                '$group': {
                    '_id': '$groups', 
                    'enrolled': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    'enrolled': -1
                }
            }
        ]
        users = self.db['users']
        unwind = users.aggregate(query)
        self.client.close()
        return query, list(unwind)
    
    def lookup(self):
        query = [
            {
                '$lookup': {
                    'from': 'hashtags', 
                    'localField': 'hashtag', 
                    'foreignField': '_id', 
                    'as': 'hashtagInfo'
                }
            }, {
                '$replaceRoot': {
                    'newRoot': {
                        '$mergeObjects': [
                            {
                                '$arrayElemAt': [
                                    '$hashtagInfo', 0
                                ]
                            }, '$$ROOT'
                        ]
                    }
                }
            }, {
                '$match': {
                    'name': 'semper'
                }
            }, {
                '$sort': {
                    'likes': -1
                }
            }, {
                '$limit': 10
            }, {
                '$group': {
                    '_id': '$name', 
                    'averageLikes': {
                        '$avg': '$likes'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'averageLikes': 1
                }
            }
        ]
        posts = self.db['posts']
        lookup = posts.aggregate(query)
        self.client.close()
        return query, list(lookup)
    
    def graphLookup(self):
        query = [
            {
                '$match': {
                    'email': 'quis.diam.luctus@ultricies.net'
                }
            }, {
                '$graphLookup': {
                    'from': 'users', 
                    'startWith': '$friends', 
                    'connectFromField': 'friends', 
                    'connectToField': 'name', 
                    'as': 'ITCs', 
                    'maxDepth': 2, 
                    'restrictSearchWithMatch': {
                        'groups': 'ITC',
                        'friends': 'Marah'
                    }
                }
            }, {
                '$project': {
                    'connections': '$ITCs._id'
                }
            }, {
                '$unwind': {
                    'path': '$connections'
                }
            }, {
                '$lookup': {
                    'from': 'posts', 
                    'localField': 'connections', 
                    'foreignField': 'user', 
                    'as': 'postInfo'
                }
            }, {
                '$sort': {
                    'postInfo.likes': -1
                }
            }, {
                '$limit': 1
            }, {
                '$unwind': {
                    'path': '$postInfo'
                }
            }, {
                '$group': {
                    '_id': None, 
                    'totalLikes': {
                        '$sum': '$postInfo.likes'
                    }
                }
            }
        ]
        users = self.db['users']
        graphLookup = users.aggregate(query)
        self.client.close()
        return query, list(graphLookup)
    
    def geoNear(self):
        query = [
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point', 
                        'coordinates': [
                            -77.73, -5.71
                        ]
                    }, 
                    'distanceField': 'distance'
                }
            }, {
                '$match': {
                    'date': {
                        '$lt': datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc), 
                        '$gte': datetime(2020, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
                    }, 
                    'likes': {
                        '$gt': 950
                    }
                }
            }, {
                '$sort': {
                    'distance': 1
                }
            }, {
                '$skip': 50
            }, {
                '$group': {
                    '_id': 'distance', 
                    'averageDistance': {
                        '$avg': '$distance'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'averageDistance': 1
                }
            }
        ]
        posts = self.db['posts']
        geoNear = posts.aggregate(query)
        self.client.close()
        return query, list(geoNear)
    
    def facet(self):
        print("PENDING")