from mongoengine import *
from datetime import datetime as dt


class Favourites(EmbeddedDocument):
    _id = StringField()
    user = StringField()
    businessName = StringField()
    phone = StringField()
    address = StringField()
    verified = BooleanField(default=False)
    cordinates = DictField()
    status = StringField(default='online')
    time_opening = StringField(default='9am')
    time_closing = StringField(default='9pm')
    kitchenImages = ListField(StringField(), default=[])
    imageUrl = StringField()
    rating_avg = IntField(default=1)
    location = DictField()
    createdAt = DateTimeField(default=dt.now())
    updatedAt = DateTimeField(default=dt.now())
    v = IntField(db_field='__v')

    def __repr__(self):
        return '<Vendor %r>' % (self.businessName)

    def toJson(self):
        return {
            '_id': self._id,
            'user': self.user,
            'cordinates': self.cordinates,
            'status': self.status,
            'time_opening': self.time_opening,
            'time_closing': self.time_closing,
            'kitchenImages': self.kitchenImages,
            'businessName': self.businessName,
            'imageUrl': self.imageUrl,
            'phone': self.phone,
            'address': self.address,
            'verified': self.verified,
            'rating_avg': self.rating_avg,
            'location': self.location,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            '__v': self.v,
        }
