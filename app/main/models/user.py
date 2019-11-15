from .. import db, flask_bcrypt
import json
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
        raise AttributeError('password: write-only field')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}' -> {}>".format(self.username, self.address)


# A specialised JSONEncoder that encodes User
# objects as JSON
class UserEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, User):
            return object.__dict__
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)

 