from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from fuudzie.models.Admin import *

from fuudzie.models.Cart import Carts
from fuudzie.models.Meal import Meals
from fuudzie.models.User import Users
from fuudzie.models.Vendor import Vendors
from fuudzie.models.Order import Orders
from fuudzie.models.Wallet import Wallets

def initializeAdmin(app):
    admin = Admin(app, name='fuudzie', template_mode='bootstrap3')
    admin.add_view(ModelView(Users))
    admin.add_view(VendorView(Vendors))
    admin.add_view(ModelView(Carts))
    admin.add_view(MealView(Meals))
    admin.add_view(OrderView(Orders))
    admin.add_view(ModelView(Wallets))
    