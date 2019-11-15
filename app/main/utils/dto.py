from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='User related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='User email address'),
        'username': fields.String(description='Username'),
        'password': fields.String(description='User password'),
        'password_hash': fields.String(description='Hashed password')
    })


class ContractDto:
    api = Namespace('contract', description='Contract related operations')
    contract = api.model('contract', {
        'name': fields.String(required=True, description='Ballot/Survey\'s name'),
        'description': fields.String(description='Description for the ballot/survey'),
        'end_date': fields.Date(required=True, description='End date of this ballot/survey')
    })