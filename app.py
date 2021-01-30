import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from src.security import authenticate, identify
from src.resources.user import UserRegister, User, UserLogin
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
from src.db import db

app = Flask(__name__) #MUST
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # data.db is in root folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turns off modification tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app) # MUST

# jwt = JWT(app, authenticate, identify)  # /auth
jwt = JWTManager(app) # not creating end-point /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
