from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identify
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db

app = Flask(__name__) #MUST
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # data.db is in root folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turns off modification tracker
app.secret_key = 'jose'
api = Api(app) # MUST

jwt = JWT(app, authenticate, identify)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
