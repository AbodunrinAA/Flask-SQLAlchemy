from flask_restful import Resource
from flask_jwt_extended import (
                jwt_required,
                fresh_jwt_required
                )

from Models import BusinessModels
from Models.BusinessModels import BusinessModel
from Security.Args import storeParser

from Models.StoreModels import StoreModel as StoreModels

# Note: Sparse is better than dense


class Store(Resource):

    # @fresh_jwt_required
    def post(self):
        """
        :param:
        :return:
        """
        try:
            response_data = storeParser.parse_args()
            if StoreModels.get_Store_By_Name(response_data['name']):
                return {'message': 'A store with name {0} already exist'.format(response_data['name'])}, 400  # Bad request

            if not BusinessModel.getBusiness_By_Id(response_data['business_id']):
                return {'message': 'The selected business does not exist'}, 400

            response_data['email'] = response_data['email'][0]
            new_resource = StoreModels(None, **response_data).insertStore()
            new_resource
            if new_resource:
                return {'message': 'Record created successfully'}, 201  # Created
            return {'message': 'Record not created successfully'}, 500  # Server Error
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error

    @fresh_jwt_required
    def put(self):
        try:
            response_data = storeParser.parse_args()

            store = StoreModels.get_Store_By_Name(response_data['name'])
            if store:
                store.name = response_data['name']
                store.updateStore()
                return {'message': 'Record updated successfully'}, 200
            StoreModels(_id=None, **response_data).insertStore()
            return {'message': 'Record created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error


class Stores(Resource):

    @jwt_required
    def get(self, name):
        """
        :param name:
        :return:
        """
        try:
            store = StoreModels.get_Store_By_Name(name)
            if store:
                return store.to_Json(), 200
            return {'message': 'Record not found'}, 404  # 200 Ok, 404 Not Found
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error

    # @fresh_jwt_required
    def delete(self, name):
        try:
            store = StoreModels.get_Store_By_Name(name)
            if store:
                store.deleteStore()
                return {'message': 'Record removed successfully'}, 200
            return {'message': 'Record not found'}, 400
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error


class StoreList(Resource):
    # @jwt_required
    def get(self):
        """
        :return:
        """
        try:
            stores = StoreModels.getAllStores()
            result_Json = [store.to_JsonNoItems() for store in
                           stores]
            return result_Json
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error


class BusinessStoreList(Resource):
    def get(self, business_id):
        """
        :return:
        """
        try:
            stores = StoreModels.get_Stores_By_Business_Id(business_id)
            result_Json = [store.to_JsonNoItems() for store in
                           stores]
            return result_Json
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error
