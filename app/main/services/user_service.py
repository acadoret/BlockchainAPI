import json
import ntpath
from datetime import datetime

from app.main import db
from app.main.models.user import User, UserEncoder
from app.main.utils.blockchain_utils import web3
from app.main.utils.dto import UserDto


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.address)
        return {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode(),
            'user' : json.dumps(user, cls=UserEncoder)
        }, 201

    except Exception as e:
        return {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }, 401

def path_leaf(path):
    """
    This delete the left part of given path
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def mass_creating(_range):
    _data= {}
    for _index in range(0,_range):
        _data['password'] = "dummy"
        _data['username'] = "dummy_{}".format(_index)
        _data['email'] = "dummy_{}".format(_index)
        _data['index'] = _index
        save_new_user(data=_data)
    return {
        'status': 'success',
        'message': '{} Users are successfully registered.'.format(_range),
    }, 201 

def save_new_user(data):
    """
    Saver in DB : This create a User object in SQLiteDB with geven parameters  
    """
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            address=web3.eth.accounts[data['index']],
            path_to_key=path_leaf('/home/antoine/Documents/pkey{}.txt'.format(data['index'])),
            password=data.get('password'),
            email=data.get('email'),
            username=data.get('username'),
            registered_on=datetime.utcnow()
        )
        save_changes(new_user)

        return generate_token(new_user)
        
    return {
        'status': 'fail',
        'message': 'User already exists. Please Log in.',
    }, 409

def get_all_users():
    print('get_all_users')
    return User.query.all()

def get_a_user(email):
    print('get_a_user')
    return User.query.filter_by(email=email).first_or_404(
        description='There is no data with {}'.format(email)
    )

def is_connected(data):
    print('is_connected')
    user = User.query.filter_by(email=data.get('email')).first()
    # Check if the given password match with the stored password
    if user and user.check_password(data['password']):
        return {
            'status' : 'success',
            'message' : 'Successfully connected.',
            'user' : json.dumps(user, cls=UserEncoder)
        }, 201
        
    return {
        'status': 'fail',
        'message': 'Incorrect login credentials. Please try again or create an account.'
    }, 409

def save_changes(data):
    print('save_changes')
    db.session.add(data)
    db.session.commit()
