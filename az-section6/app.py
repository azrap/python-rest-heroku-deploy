from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
# make sure you import all resources for tables you want built:
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from security import authenticate, identity
from datetime import timedelta
from db import db

app = Flask(__name__)
# To allow flask propagating exception even if debug is set to false on app
app.config['PROPAGATE_EXCEPTIONS'] = True

# SQL alchemy config, connection to the DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

# this will get run before the first ever request and will create all the tables that don't exist
@app.before_first_request
def create_tables():
    db.create_all()


# if we don't specify the below, it defaults to /auth as endpoint for login
# app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=30)


items = []
stores = []

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


# only the file that you run is supposed to be main
# if you don't put main, that means it's imported and we don't want to run it
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)  # important to mention debug=True
