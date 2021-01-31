from flask_restful import Resource, reqparse
from flask_jwt_extended import *
from src.models.item import ItemModel
from src.models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be lef blank."
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with '{}' already exists".format(name)}, 400

        jsonPayload = Item.parser.parse_args()

        if StoreModel.find_by_id(jsonPayload['store_id']) is None:
            return {'message':'There is no Store. You should be add store first.'}, 400

        item = ItemModel(name, **jsonPayload)

        try:
            item.save_to_db() # attributing object self
        except:
            return {"message", "An error occurred inserting the item"}

        return item.json(), 201  # create success

    @jwt_required
    def delete(self, name):
        # using JWT claim
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {'message':'Item deleted'}
        return {'message':'Item no found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.query.all()]

        if user_id:
            return {'items':items}, 200

        return {'items': [item['name'] for item in items],
                'message':'More data available if you log-in'
                }

    def delete(self):
        ItemModel.delete_all_data_from_db()
        return {'message':'all item is successfully deleted.'}
