
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy as sa
import datetime
import json

from api.common.database import db

# https://github.com/oliverSI/flask-restful-authentication


class UserModel(db.Model):
    __tablename__ = "users"
    USERNAME_FORMAT = "^[A-Za-z0-9_-]+?$"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(600), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, server_default=sa.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    _roles = db.Column("roles", db.String(255), nullable=False, default="[]", server_default="[]")
    
    @hybrid_property
    def roles(self):
        return json.loads(self._roles)

    @roles.setter
    def roles(self, roles):
        self._roles = json.dumps(roles)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    # User information to save in JWT token
    def jwt_serialize(self):
        return {
            'id':self.id,
            'username':self.username, 
            'roles':self.roles
        }

    @classmethod
    def find_by_username(cls, username, exclude_deleted = True):
        q = cls.query.filter(UserModel.username == username)
        if exclude_deleted:
            q.filter(UserModel.deleted_at != None)
        return q.first()

    @classmethod
    def find_by_email(cls, email, exclude_deleted=True):
        q = cls.query.filter(UserModel.email == email)
        if exclude_deleted:
            q.filter(UserModel.deleted_at != None)
        return q.first()

    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password, salt_length=256)
    
    @staticmethod
    def verify_hash(password, hash):
        return check_password_hash(hash, password)

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


