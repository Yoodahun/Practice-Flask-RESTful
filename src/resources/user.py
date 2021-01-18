import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connnection = sqlite3.connect('data.db')
        cursor = connnection.cursor()

        # parameter always should be tuple
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()  # get the first row data

        if row:
            user = cls(*row)  # id, username, password
        else:
            user = None

        return user

    @classmethod
    def find_by_id(cls, _id):
        connnection = sqlite3.connect('data.db')
        cursor = connnection.cursor()

        # parameter always should be tuple
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()  # get the first row data

        if row:
            user = cls(*row)  # id, username, password
        else:
            user = None

        return user


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
            return {"message" : "A User with that username already exists"}, 400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message" : "User created successfully"}, 201
