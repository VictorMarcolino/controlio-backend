from flask import Blueprint, jsonify
health = Blueprint('health', __name__)


@health.route('/liveness')
def liveness():
    response = jsonify({"status": 200})
    response.headers['Content-Type'] = 'application/json'
    return response, 200


@health.route('/readiness')
def readiness():
    response = jsonify({"status": 200})
    response.headers['Content-Type'] = 'application/json'
    return response, 200
