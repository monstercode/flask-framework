from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_claims
from flask_cors import CORS
import click

from api.config.config import config
from api.common.database import db

#from resources.project import Project as ProjectResource
#from resources.project import Project as ProjectResource


app = Flask(__name__)
app.config.update(config)
#auth = BasicRoleAuth()


api = Api(app)
db.init_app(app)

migrate = Migrate(app, db)
jwt = JWTManager(app)
# https://github.com/corydolphin/flask-cors
#cors = CORS(app, resources={r"*": {"origins": config['CORS_ORIGINS']}})

from api.resources.auth import UserRegistration
from api.resources.auth import UserRegistration
from api.resources.auth import UserLogin
from api.resources.auth import UserLogoutAccess
from api.resources.auth import UserLogoutRefresh
from api.resources.auth import TokenRefresh
from api.resources.auth import SecretResource
from api.resources.file import File


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

#api.add_resource(ProjectResource, '/projects/<string:id>')

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserLogoutAccess, '/auth/logout')
api.add_resource(UserLogoutRefresh, '/auth/logout-refresh')
api.add_resource(TokenRefresh, '/auth/refresh')
api.add_resource(SecretResource, '/jwt-test')

api.add_resource(File, '/uploads')
