import sqlite3
from flask_restful import Resource, reqparse
from models.user import User


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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A User with that username already exists"}, 400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
