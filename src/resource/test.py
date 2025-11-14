from flask_restful import Resource
from flask import jsonify

class TestResource(Resource):
    def get(self):
        return jsonify({"message": "This is a test message"})