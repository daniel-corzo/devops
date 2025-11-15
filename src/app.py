from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from datetime import datetime
from src.config import Config
from src.resource.black_lists_resource import (
    BlackListsResource,
    BlackListsEmailResource,
)
from src.resource.auth import AuthResource
from src.resource.test import TestResource
from src.models import Base, engine

app = Flask(__name__)
app.config.from_object(Config)

# Initialize JWT
jwt = JWTManager(app)


# JWT Error handlers
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({"message": "Token is required"}), 403


@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({"message": "Invalid token"}), 403


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Token has expired"}), 403


# Handle NoAuthorizationError exception
@app.errorhandler(NoAuthorizationError)
def handle_no_authorization_error(e):
    return jsonify({"message": "Token is required"}), 403


@app.route("/health", methods=["GET"])
def health():
    return jsonify({}), 500
    # return jsonify({
    #     "timestamp": datetime.now().isoformat()
    # })

Base.metadata.create_all(engine)
api = Api(app)

api.add_resource(BlackListsResource, "/blacklists")
api.add_resource(BlackListsEmailResource, "/blacklists/<string:email>")
api.add_resource(AuthResource, "/auth/token")
api.add_resource(TestResource, "/test-res")

if __name__ == "__main__":
    app.run(debug=True)
