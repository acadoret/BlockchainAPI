import ntpath
import json
from datetime import datetime
from os import urandom

from ..utils.blockchain_utils import web3
from eth_account import Account

from app.main import db
from app.main.models.user import User, UserEncoder

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def save_new_user(data):
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
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
        
    return {
        'status': 'fail',
        'message': 'User already exists. Please Log in.',
    }, 409


def get_all_users():
    # print(User.query.all())
    return User.query.all()


def get_a_user(address):
    return User.query.filter_by(address=address).first()

def is_connected(data):
    print(data['password'])
    user = User.query.filter_by(email=data['email']).first()
    print(user.__dict__)
    if user.check_password(data['password']):
        print('OKKKKKKKKKKKKKKKKKK' + str(type(user)))
        print('zemflkzjgnklerjrkemrljerklrjkl' + str(type({'foo': 'foo','dummy' : ['a','a']})))
        return {
            'status' : 'success',
            'message' : 'Successfully connected.',
            'user' : json.JSONEncoder.encode([{'foo': 'foo','dummy' : ['a','a']}])
        }, 201
        
    return {
        'status': 'fail',
        'message': 'Incorrect login credentials. Please try again or create an account.'
    }, 409

def save_changes(data):
    db.session.add(data)
    db.session.commit()