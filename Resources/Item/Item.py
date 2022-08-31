from flask_restful import Resource
from flask_jwt_extended import (
                jwt_required,
                fresh_jwt_required
                )
from Models.ItemModels import ItemModel as ItemModels
from Security.Args import itemParser
from Models.StoreModels import StoreModel


# Post
class Item(Resource):

    # @fresh_jwt_required
    def post(self):
        """
        :param:
        :return:
        """
        response_data = itemParser.parse_args()
        try:
            if ItemModels.get_Item_By_Name(response_data['name']):
                return {'message': 'An item with name {0} already exist'.format(response_data['name'])},\
                       400  # Bad request

            if not StoreModel.get_Store_By_Id(response_data['store_id']):
                return {'message': 'The selected store does not exist'}, 400
            new_resource = ItemModels(None, **response_data).insertItem()
            if new_resource:
                return {'message': 'Record created successfully'}, 201  # Created
            return {'message': 'Record not created successfully'}, 500  # Server Error
        except:
            return {'message': 'Server Error, Do try again'}, 500  # Server Error

    @fresh_jwt_required
    def put(self):
        try:
            response_data = itemParser.parse_args()

            item = ItemModels.get_Item_By_Name(response_data['name'])
            if item:
                item.price = response_data['price']
                item.store_id = response_data['store_id']
                item.expire_date = response_data['expire_date']
                item.produce_date = response_data['produce_date']
                item.updateItem()
                return {'message': 'Record updated successfully'}, 200

            ItemModels(_id=None, **response_data).insertItem()
            return {'message': 'Record created successfully'}, 201
        except:
            return {'message': 'Server Error, Do try again'}


class Items(Resource):
    @jwt_required
    def get(self, name):
        """
        :param name:
        :return:
        """

        item = ItemModels.get_Item_By_Name(name)
        if item:
            return item.to_Json(), 200
        return {'message': 'Record not found'}, 404  # 200 Ok, 404 Not Found

    @fresh_jwt_required
    def delete(self, name):
        try:
            item = ItemModels.get_Item_By_Name(name)
            if item:
                item.deleteItem()
                return {'message': 'Record removed successfully'}, 200
            return {'message': 'Record not found'}, 400
        except:
            return {'message': 'Server Error, Do try again'}, 500


class ItemList(Resource):
    @fresh_jwt_required
    def get(self):
        """
        :return:
        """
        items = ItemModels.getAllItems()
        result_Json = [item.to_Json() for item in
                       items]
        return result_Json
