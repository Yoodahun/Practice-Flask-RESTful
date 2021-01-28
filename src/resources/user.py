from flask_restful import Resource, reqparse
from src.models.user import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be lef blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be lef blank."
                        )

    def post(self):

        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A User with that username already exists"}, 400

        user = User(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201


class Users(Resource):

    @classmethod
    def get(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message':'User not found'}, 404

        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        user.delete_from_db()
        return {'message':'User deleted successfully.'}, 200