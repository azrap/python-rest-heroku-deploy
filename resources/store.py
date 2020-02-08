from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #                     type=str,
    #                     required=True,
    #                     help="Store name cannot be blank."
    #                     )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200

        return {'message': 'Store not found'}, 404

    def post(self, name):
        print('store name', name)
        if StoreModel.find_by_name(name):
            return {'message': f'Store with name {name} already exists'}, 400

        # data = Store.parser.parse_args()

        store = StoreModel(name)

        try:
            store.save_to_db()
            return store.json()
        except:
            return {"message": "An error occurred inserting the store."}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted'}
        return {'message': 'Store not found'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
