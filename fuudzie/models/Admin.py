from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import rules

class UserView(ModelView):
    pass

class OrderView(ModelView):
    pass

class CartView(ModelView):

    form_subdocuments = {
        'cartItems': {
            'form_subdocuments':{
                None: {
                    'form_rules': ('_id', 'name', rules.HTML('<hr>')),
                    'form_widget_args': {
                        'name': {
                            'style': 'color: red'
                        }
                    }
                }
            }
        }
    }

class VendorView(ModelView):
    pass


class EscrowView(ModelView):
    pass

class MealView(ModelView):
    pass