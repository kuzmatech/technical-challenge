from os import environ
from flask import Flask, Response, make_response, jsonify, request
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from storage import StorageInstance
from handlers import authenticator

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = environ.get('TC_SECRET_KEY')
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
api = Api(app, prefix="/api")
authenticate = authenticator.check_login_details
identity = authenticator.identity
StorageInstance()
jwt = JWT(app, authenticate, identity)
@app.errorhandler(403)
def forbidden(msg):
    return make_response(jsonify({"message": msg}), 403)

if __name__ == '__main__':
  from storage import User
  try:
    User.get(User.username == "test_user")
  except User.DoesNotExist:
    User.add_user("test_user", "example_pass_5")
  app.run(host='127.0.0.1', port=4924, debug=True)
  # {TODO}:
  # Populate products.json into database
