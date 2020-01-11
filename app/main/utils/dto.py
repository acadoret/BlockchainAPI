from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='User related operations')
    user = api.model('user', {
        'email': fields.String(description='User email address'),
        'username': fields.String(description='Username'),
        'address': fields.String(description='User address'),
        'password_hash': fields.String(description='Hashed password'),
        'password': fields.String(description='password'),
    })


class ContractDto:
    api = Namespace('contract', description='Contract related operations')
    proposal = api.model('proposal', {
        'index': fields.Integer(description="Index in Blockchain"),
        'name': fields.String(description="Name of proposal"),
        'vote_count': fields.Integer(description="Number of vote"),
        'is_winning': fields.Integer(description="This proposal is winning ?"),
    })
    contract = api.model('contract', {
        'address': fields.String(description='Contract\'s address'),
        'user_address': fields.String(description='User\'s address who create contract'),
        'name': fields.String(description='Ballot/Survey\'s name'),
        'description': fields.String(description='Description for the ballot/survey'),
        'end_date': fields.Date(description='End date of this ballot/survey'),
        'proposals': fields.List(fields.String(description="Proposal names for insert")),
        '_proposals': fields.List(
            fields.Nested(proposal,description="Choices of Contract")
        )
    })

class AuthDto:
    api = Namespace('auth', description='Authentification related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

    