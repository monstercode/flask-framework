from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_claims
from flask_cors import CORS
import click

from api.config.config import config
from api.common.database import db

app = Flask(__name__)
app.config.update(config)
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# https://github.com/corydolphin/flask-cors
#cors = CORS(app, resources={r"*": {"origins": config['CORS_ORIGINS']}})

# Define JWT Content with dict
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'id': identity['id'],
        'username': identity['username'],
        'roles': identity['roles'],
    }

@api.representation('image/*')
@api.representation('application/octet-stream')
def binary(data, code, headers=None):
    # if data is already a respose return data
    return data
    # else make response with data
    # resp = api.make_response(data, code)
    # resp.headers.extend(headers or {})
    # return resp

import api.routes
