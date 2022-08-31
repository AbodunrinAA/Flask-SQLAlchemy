from flask_restful import Resource
from Security.Args import userParser
from werkzeug.security import check_password_hash, generate_password_hash  # safe_str_cmp,
from Models.StoreModels import StoreModel
import datetime
from Models.UserModels import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    fresh_jwt_required,
    jwt_required,
    get_jwt_identity,  # This return Login User Identity
    get_raw_jwt,
)
from Security.blacklist import BLACKLIST


class User(Resource):
    # Create User
    @classmethod
    def post(cls):
        try:
            response_data = userParser.parse_args()
            response_data['username'] = response_data['username'][0]
            if UserModel.getUser_By_Username(response_data['username']):
                return {'message': 'User with the same Username already exist'}, 400  # Bad Request

            if not StoreModel.get_Store_By_Id(response_data['store_id']):
                return {'message': 'The selected store does not exist'}, 400
            # This hash the password
            response_data['password'] = generate_password_hash(response_data['password'])

            user = UserModel(None, **response_data)
            user.insertUser()
            return {'message': 'Record created successfully'}, 201  # Created
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error


class Users(Resource):
    # Get User
    # @jwt_required
    def get(self, username: str):
        try:
            user = UserModel.getUser_By_Username(username)
            if user:
                return user.to_Json(), 200
            return {'message': 'Record not found'}, 400
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error

    @classmethod
    # Delete User
    def delete(cls, username: str):
        user = UserModel.getUser_By_Username(username)
        if not user:
            return {"message": "User not found."}, 404
        user.delete()
        return {"message": "User deleted."}, 200


class DeleteUser(Resource):
    @classmethod
    # Delete User
    @fresh_jwt_required
    def delete(cls):
        identity_user_id = get_jwt_identity()
        user = UserModel.getUser_By_Id(identity_user_id)
        if not user:
            return {"message": "User not found."}, 404
        user.delete()
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "User deleted."}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        response_data = userParser.parse_args()
        response_data['username'] = response_data['username'][0]

        user = UserModel.getUser_By_Username(response_data["username"])
        if user and check_password_hash(user.password, response_data["password"]):
            access_token = create_access_token(identity=user.id,
                                               fresh=True,
                                               expires_delta=datetime.timedelta(minutes=5))
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials!"}, 400  # Bad request


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "User <id={}> successfully logged out.".format(user_id)}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class UserList(Resource):

    def get(self):
        try:
            users = UserModel.getAllUsers()
            users = [user.to_Json() for user in users]
            return users
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error


class StoreUserList(Resource):
    def get(self, store_id):
        try:
            users = UserModel.getUser_By_store_id(store_id)
            users = [user.to_Json() for user in users]
            return users
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error
