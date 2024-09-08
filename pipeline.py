from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('MONGODB_HOST')
db_name = os.getenv('MONGODB_DB') 
collection_name = os.getenv('MONGODB_COLLECTION') 

def get_stats_by_device(device_id,start_date, end_date, filter):
    client = MongoClient(uri)
    if(client):
        print("MongoDB Connected")
    try:
        db = client[db_name]
        collection = db[collection_name]
        pipeline = [
            {
                '$match': {
                    'deviceId': device_id,
                    'created': {'$gte': start_date, '$lte': end_date}
                }
            },
            {
                '$sort': {'value': -1}
            },
            {
                '$group': {
                    '_id': {
                        'deviceId': '$deviceId',
                        'year': {'$year': '$created'},
                        'month': {'$month': '$created'},
                        'day': {'$dayOfMonth': '$created'},
                        'hour': {'$hour': '$created'}
                    },
                    'max': {'$first': '$value'},
                    'maxDate': {'$first': '$created'},
                    'min': {'$last': '$value'},
                    'minDate': {'$last': '$created'},
                    'created': {'$max': '$created'},
                    'avg': {'$avg': '$value'}
                }
            },
            {
                '$sort': {'_id': -1}
            },
            {
                '$project': {
                    '_id': 0,
                    'max': {'value': '$max', 'created': '$maxDate'},
                    'min': {'value': '$min', 'created': '$minDate'},
                    'avg': {'$round': ['$avg', 0]},
                    'created': '$created'
                }
            }
        ]

        if filter == 'daily':
            del pipeline[2]['$group']['_id']['hour']
        elif filter == 'monthly':
            del pipeline[2]['$group']['_id']['hour']
            del pipeline[2]['$group']['_id']['day']

        result = list(collection.aggregate(pipeline))

        return result

    finally:
        client.close()



