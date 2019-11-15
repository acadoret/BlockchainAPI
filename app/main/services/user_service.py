import json
import ntpath
from datetime import datetime
from json.encoder import JSONEncoder
from os import urandom

from eth_account import Account

from app.main import db
from app.main.models.user import User, UserEncoder

from ..utils.blockchain_utils import web3
from ..utils.dto import UserDto


def path_leaf(path):
    """
    This delete the left part of given path
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def save_new_user(data):
    """
    Saver in DB : This create a User object in SQLiteDB with geven parameters  
    """
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        new_user = User(
            address=web3.eth.accounts[4],
            path_to_key=path_leaf('/home/antoine/Documents/pkey4.txt'),
            password=data['password'],
            email=data['email'],
            username=data['username'],
            registered_on=datetime.utcnow()
        )
        save_changes(new_user)
        return {
            'status': 'success',
            'message': 'Successfully registered.',
            'user' : json.dumps(new_user, cls=UserEncoder)
        }, 201
        
    return {
        'status': 'fail',
        'message': 'User already exists. Please Log in.',
    }, 409

def get_all_users():
    print('get_all_users')
    return User.query.all()

def get_a_user(email):
    print('get_a_user')
    return User.query.filter_by(email=email).first()

def is_connected(data):
    print('is_connected')
    user = User.query.filter_by(email=data['email']).first()
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
