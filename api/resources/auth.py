from flask_restful import reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import re, json

from api.common.resources import BaseResource, ProtectedResource
from api.models.user import UserModel, RevokedTokenModel
from api.common.authorization import has_role

class UserRegistration(ProtectedResource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'This field cannot be blank', location='json', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', location='json', required = True)
        parser.add_argument('email', help = 'This field cannot be blank', location='json', required = True)
        data = parser.parse_args()

        if not re.match(UserModel.USERNAME_FORMAT, data['username']):
            return {'message': 'Username must consist of letters, numbers, hyphens and underscores'}

        if UserModel.find_by_username(username=data['username'], exclude_deleted=False):
            return {'message': 'Username {} already exists'.format(data['username'])}
        
        if UserModel.find_by_email(email=data['email'], exclude_deleted=False):
            return {'message': 'User with email {} already exists'.format(data['email'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            email = data['email'],
            deleted_at = None,
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(new_user.jwt_serialize() )
            refresh_token = create_refresh_token(new_user.jwt_serialize())
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 400


class UserLogin(BaseResource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'This field cannot be blank', location='json', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', location='json', required = True)
        data = parser.parse_args()

        if not re.match(UserModel.USERNAME_FORMAT, data['username']):
            return {'message': 'User not found'}

        current_user = UserModel.find_by_username(username=data['username'], exclude_deleted=True)
        if not current_user or current_user.deleted_at != None:
            return {'message': 'User {} not found'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(current_user.jwt_serialize())
            refresh_token = create_refresh_token(current_user.jwt_serialize())
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(ProtectedResource):
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(BaseResource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(BaseResource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}



# Just for testing
class SecretResource(ProtectedResource):
    @jwt_required
    @has_role('admin')
    def get(self):
        return {'message': 'Success! JWT verified'}
