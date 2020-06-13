''' controller and routes for users '''
import os
import pandas as pd
from flask import request, jsonify, render_template
from app import app, listings
import logger
import re

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/country', methods=['POST'])
def country_price():
    # country = request.form.to_dict()
    # all_listing_in_country = listings.find(
    #     country, projection={"_id": False, "price": True})
    all_listing_in_country = listings.aggregate([{
        "$group": {
            "_id": "$address.country",
            "mean_price": {
                "$avg": "$price"
            }
        }
    }])
    all_listing_in_country = list(all_listing_in_country)
    keys = []
    vals = []
    for c in all_listing_in_country:
        print(c["_id"])
        keys.append(c["_id"])
        vals.append(c["mean_price"])
    res = dict(zip(keys, vals))
    return jsonify(res)


@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    print("request", request.method)
    # if request.method == 'GET':
    #     query = request.args
    #     print("args", request.args)
    #     data = listings.find_one(query)
    #     return jsonify(data), 200
    # data = request.get_json(force=True)
    res = ""
    if request.method == 'POST':
        query = request.form.to_dict()
        conditions = []
        for key in query.keys():
            conditions.append(key)
        # query.pop('submitType')
        print("summary!!!!!:", conditions)

        summary = listings.find({"amenities": {"$all": conditions}})

        summary = list(summary)
        # print("result!!!", summary)
        # summary = listings.find({"ameni": {"$all": ["red", "blank"]}}, limit=200)
        df = pd.DataFrame(summary)
        # print('dataf!rame', df['summary'].tolist())
        text = df['summary'].tolist()
        # res = []
        freqMap = {}
        for item in text:
            curr = item.split(" ")
            for c in curr:
                c = re.sub(r'[^\w]', ' ', c)
                c = c.lower()
                if c.isnumeric() or len(c) <= 3:
                    continue
                else:
                    freqMap[c] = freqMap.get(c, 0) + 1
        freqMap = {k: v for k, v in sorted(
            freqMap.items(), key=lambda x: x[1], reverse=True)}
        toRemove = list(freqMap)[400:]
        for r in toRemove:
            del freqMap[r]

        for stop in ['with', 'this', 'where', 'there', 'from', 'also', 'just']:
            del freqMap[stop]
        print(freqMap)
        return jsonify(freqMap), 200
        #     return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
        # else:
        #     return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    # if request.method == 'DELETE':
    #     if data.get('email', None) is not None:
    #         db_response = listings.delete_one({'email': data['email']})
    #         if db_response.deleted_count == 1:
    #             response = {'ok': True, 'message': 'record deleted'}
    #         else:
    #             response = {'ok': True, 'message': 'no record found'}
    #         return jsonify(response), 200
    #     else:
    #         return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    # if request.method == 'PATCH':
    #     if data.get('query', {}) != {}:
    #         listings.update_one(
    #             data['query'], {'$set': data.get('payload', {})})
    #         return jsonify({'ok': True, 'message': 'record updated'}), 200
    #     else:
    #         return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
