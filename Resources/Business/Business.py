from flask_restful import Resource
from flask_jwt_extended import (
                jwt_required,
                fresh_jwt_required
                )
from Security.Args import businessParser

from Models.BusinessModels import BusinessModel as BusinessModels

# Note: Sparse is better than dense


class Business(Resource):

    # @fresh_jwt_required
    def post(self):
        """
        :param:
        :return:
        """
        try:
            response_data = businessParser.parse_args()
            if BusinessModels.get_Business_By_Name(response_data['name']):
                return {'message': 'A Business with name {0} already exist'.format(response_data['name'])}, 400

            new_resource = BusinessModels(None, **response_data).insertBusiness()
            if new_resource:
                return {'message': 'Record created successfully'}, 201  # Created
            return {'message': 'Record not created successfully'}, 500  # Server Error
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error


class Businesses(Resource):
    # @jwt_required
    def get(self, name):
        """
        :param name:
        :return:
        """
        try:
            store = BusinessModels.get_Business_By_Name(name)
            if store:
                return store.to_Json(), 200
            return {'message': 'Record not found'}, 404  # 200 Ok, 404 Not Found
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error

    # @fresh_jwt_required
    def delete(self, name):
        try:
            store = BusinessModels.get_Business_By_Name(name)
            if store:
                store.delete()
                return {'message': 'Record removed successfully'}, 200
            return {'message': 'Record not found'}, 400
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error


class BusinessList(Resource):
    # @jwt_required
    def get(self):
        """
        :return:
        """
        try:
            stores = BusinessModels.getAllBusinesses()
            result_Json = [store.to_Json() for store in
                           stores]
            return result_Json
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error