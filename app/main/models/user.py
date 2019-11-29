import datetime
import json

import jwt

from app.main.models.blacklist_token import BlacklistToken
from sqlalchemy.ext.declarative import DeclarativeMeta

from .. import db, flask_bcrypt
from ..config import key

print("User Model: {}".format(key))

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    address = db.Column(db.String(42), primary_key=True)
    path_to_key = db.Column(db.String(1024), index=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    
    contract_ids = db.relationship("Contract", back_populates="user")
    
    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    @password.getter
    def password(self):
        # raise AttributeError('password: write-only field')
        return False

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
            """
            Generates the Auth Token
            :return: string
            """
            try:
                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                    'iat': datetime.datetime.utcnow(),
                    'sub': user_id
                }
                return jwt.encode(payload,key,algorithm='HS256')

            except Exception as e:
                return e

    @staticmethod  
    def decode_auth_token(auth_token):
            """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
            """
            try:
                print("\r\n AUTH {}\r\n KEY {} \r\n".format(auth_token, key))
                payload = jwt.decode(auth_token, key,algorithm='HS256')
                is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
                if is_blacklisted_token:
                    return 'Token blacklisted. Please log in again.'
                else:
                    print("Payload sub: {}".format(payload['sub']))
                    return payload['sub']
            except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.'
            except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}' -> {}>".format(self.username, self.address)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# A specialised JSONEncoder that encodes User
# objects as JSON
class UserEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and 'password' not in x]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
