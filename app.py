import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from src.security import authenticate, identify
from src.resources.user import UserRegister, User, UserLogin, TokenRefresh
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
from src.db import db

app = Flask(__name__) #MUST
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # data.db is in root folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turns off modification tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose' # app.config['JWT_SECRET_KEY']
api = Api(app) # MUST


@app.before_first_request
def create_tables():
    db.create_all()

# jwt = JWT(app, authenticate, identify)  # /auth
jwt = JWTManager(app) # not creating end-point /auth

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Instead of hard-coding, should read from a config file or DB
        return {'is_admin': True}
    return {'is_admin':False}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
