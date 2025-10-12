from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token


class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        identity = data.get("identity")
        token = create_access_token(identity=identity)
        return {"access_token": token, "token_type": "Bearer"}, 200
