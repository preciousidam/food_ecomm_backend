from flask.json import JSONEncoder
from bson import ObjectId
from datetime import datetime as dt
from fuudzie.models.Meal import MealEmbedded
from fuudzie.models.Meal import Meals
from fuudzie.models.Vendor import Vendors
from fuudzie.models.User import Users
from fuudzie.models.Escrow import Escrows
from fuudzie.models.Order import Orders
from fuudzie.models.Cart import Carts
from fuudzie.models.Wallet import Wallets
from fuudzie.models.Transaction import Transactions

class JSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, dt):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o,MealEmbedded):
            return o.toJson()
        if isinstance(o,Meals):
            return o.toJson()
        if isinstance(o,Users):
            return o.toJson()
        if isinstance(o,Vendors):
            return o.toJson()
        if isinstance(o,Carts):
            return o.toJson()
        if isinstance(o,Wallets):
            return o.toJson()
        if isinstance(o,Orders):
            return o.toJson()
        if isinstance(o,Transactions):
            return o.toJson()
        if isinstance(o,Escrows):
            return o.toJson()
        
        return JSONEncoder.default(self, o)