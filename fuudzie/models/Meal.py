from mongoengine import *
from datetime import datetime

from fuudzie.models.Vendor import Vendors

class Meals(Document):
    vendor = ReferenceField(Vendors, reverse_delete_rule=CASCADE)
    name = StringField()
    description = StringField()
    orderType = StringField()
    orderSize = StringField()
    pricePerOrderSize = FloatField()
    cordinates = DictField()
    businessName = StringField()
    businessLocation = DictField()
    mealImages = ListField(StringField())
    quantity = IntField(default=1)
    timeToPrepare = IntField()
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField(default=datetime.now())
    v = IntField(db_field='__v')


    def __repr__(self):
        return 'Meals %r' % (self.name)

    def toJson(self):
        return {
            '_id': self.pk,
            'vendor': self.vendor,
            'name': self.name,
            'description': self.description,
            'orderType': self.orderType,
            'orderSize': self.orderSize,
            'pricePerOrderSize': self.pricePerOrderSize,
            'cordinates': self.cordinates,
            'businessName': self.businessName,
            'businessLocation': self.businessLocation,
            'mealImages': self.mealImages,
            'quantity': self.quantity,
            'timeToPrepare': self.timeToPrepare,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            '__v': self.v,
        }

class MealEmbedded(EmbeddedDocument):
    _id = StringField()
    vendor = ReferenceField(Vendors)
    name = StringField()
    description = StringField()
    orderType = StringField()
    orderSize = StringField()
    pricePerOrderSize = FloatField()
    cordinates = DictField()
    businessName = StringField()
    businessLocation = DictField()
    mealImages = ListField(StringField())
    quantity = IntField(default=1)
    timeToPrepare = IntField()
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField(default=datetime.now())


    def __repr__(self):
        return 'Meals %r' % (self.name)

    def toJson(self):
        return {
            '_id': self._id,
            'vendor': self.vendor,
            'name': self.name,
            'description': self.description,
            'orderType': self.orderType,
            'orderSize': self.orderSize,
            'pricePerOrderSize': self.pricePerOrderSize,
            'cordinates': self.cordinates,
            'businessName': self.businessName,
            'businessLocation': self.businessLocation,
            'mealImages': self.mealImages,
            'quantity': self.quantity,
            'timeToPrepare': self.timeToPrepare,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
        }