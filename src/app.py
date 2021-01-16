from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identify
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__) #MUST
app.secret_key = 'jose'
api = Api(app) # MUST

jwt = JWT(app, authenticate, identify)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)