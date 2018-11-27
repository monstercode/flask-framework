from flask_cors import CORS

from api.app import api, app
from api.config.config import config

# https://github.com/corydolphin/flask-cors
cors = CORS(app, resources={r"*": {"origins": config['CORS_ORIGINS']}})

from api.resources.auth import UserRegistration
from api.resources.auth import UserRegistration
from api.resources.auth import UserLogin
from api.resources.auth import UserLogoutAccess
from api.resources.auth import UserLogoutRefresh
from api.resources.auth import TokenRefresh
from api.resources.auth import SecretResource
from api.resources.file import File

## Authentication ## 
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout')
api.add_resource(UserLogoutRefresh, '/logout-refresh')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(SecretResource, '/jwt-test')

## File Management ##
api.add_resource(File, '/uploads')
