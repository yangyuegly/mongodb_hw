''' controller and routes for users '''
import os
from flask import request, jsonify, render_template
from app import app, listings
import logger
ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    print("request", request.method)
    # if request.method == 'GET':
    #     query = request.args
    #     print("args", request.args)
    #     data = listings.find_one(query)
    #     return jsonify(data), 200
    # data = request.get_json(force=True)
    if request.method == 'POST':
        print("reach", request.form.to_dict())
        query = request.form.to_dict()
        query.pop('submitType')
        print("query", query)
        data = listings.find_one(query)
        return jsonify(data), 200
        #     return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
        # else:
        #     return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = listings.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            listings.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
