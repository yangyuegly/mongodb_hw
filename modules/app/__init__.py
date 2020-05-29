''' flask app with mongo '''
''' flask app with mongo '''
# create the flask object
from flask_pymongo import pymongo
import os
import json
from decimal import Decimal
from bson.decimal128 import Decimal128, create_decimal128_context
import datetime
from bson.objectid import ObjectId
from flask import Flask

class JSONEncoder(json.JSONEncoder):                           
    ''' extend json-encoder class'''
    def default(self, o):                               
        if isinstance(o, ObjectId):
            return str(o)                               
        if isinstance(o, datetime.datetime):
            return str(o)
        if isinstance(o, Decimal128):
            return str(o)
        if isinstance(o, Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

CONNECTION_STRING = "mongodb://dbuser:data1050@cluster0-shard-00-00-isyxr.mongodb.net:27017,cluster0-shard-00-01-isyxr.mongodb.net:27017,cluster0-shard-00-02-isyxr.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('sample_airbnb')
listings = pymongo.collection.Collection(db, 'listingsAndReviews')


# add mongo url to flask config, so that flask_pymongo can use it to make connection


# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.json_encoder = JSONEncoder

from app.controllers import *