from flask import request
from flask_restplus import Resource

from app.main.utils.dto import UserDto
from app.main.services.user_service import save_new_user, get_all_users, get_a_user, is_connected, mass_creating
from app.main.utils.decorators import token_required, admin_token_required
api = UserDto.api
_user = UserDto.user


@api.route('/all', methods=['GET'])
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()


@api.route('/<email>', methods=['GET'])
@api.param('email', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    @token_required
    def get(self, email):
        """get a user given its identifier"""
        user = get_a_user(email)
        if not user:
            api.abort(404)
        else:
            return user

@api.route('/create', methods=['POST'])
class UserCreate(Resource):
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    @token_required
    def post(self):
        """ Create a new User """
        # TODO: Faire la partie création wallet 
        # ETH et placer l'@ETH dans data 
        data = request.json
        if data.get('range'):
            return mass_creating(data.get('range'))

        return save_new_user(data=data)

# @api.route('/auth', methods=['POST'])
# @api.param('email', 'The User identifier')
# @api.param('password', 'His password')
# @api.response(404, 'Incorrect login credentials.')
# class AuthUser(Resource):
#     @api.response(201, 'User successfully logged.')
#     @api.doc('Log a user')
#     @api.expect(_user, validate=True)
#     def post(self):
#         """Authentificate a user"""
#         return is_connected(request.json)
