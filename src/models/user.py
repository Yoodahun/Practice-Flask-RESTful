import sqlite3
from ..db import db


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


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
