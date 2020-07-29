from bson.json_util import loads, dumps
from mongoengine import *
from datetime import datetime

from fuudzie.models.User import Users
from fuudzie.models.Meal import *


class Carts(Document):
    user = ReferenceField(Users, reverse_delete_rule=CASCADE)
    cartItems= EmbeddedDocumentListField(MealEmbedded)
    totalQuantity = IntField()
    totalPrice = FloatField()
    status = StringField()
    deliveryFee= FloatField()
    fixedFee = BooleanField()
    deliveryLocation = DynamicField()
    feesPerVendor = DictField()
    createdAt = DateTimeField(default=datetime.utcnow())
    updatedAt = DateTimeField(default=datetime.utcnow())
    v = IntField(db_field='__v')

    def __repr__(self):
        
        return '<Cart for %r>' % (self.user.email)

    def toJson(self):
        return {
            '_id' : self.pk,
            'user' : self.user,
            'cartItems' : self.cartItems,
            'totalQuantity' : self.totalQuantity,
            'status' : self.status,
            'totalPrice': self.totalPrice,
            'deliveryFee': self.deliveryFee,
            'fixedFee' : self.fixedFee,
            'deliveryLocation' : self.deliveryLocation,
            'createdAt' : self.createdAt,
            'updatedAt' : self.updatedAt,
            '__v': self.v,
        }


    