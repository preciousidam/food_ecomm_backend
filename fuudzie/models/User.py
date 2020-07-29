from mongoengine import *
from datetime import datetime as dt

from fuudzie.models.Embedded import Favourites


class Users(Document):
    firstName = StringField()
    lastName = StringField()
    password = StringField(min_value=6, max_value=255)
    email = EmailField(unique=True)
    lastLogin = DateTimeField(default=dt.now())
    dateOfBirth = DateTimeField()
    phone = StringField()
    resetPasswordToken = StringField()
    resetPasswordExpires = FloatField()
    role = ListField(StringField())
    token = StringField()
    imageUrl = StringField()
    address = StringField()
    cordinates = DictField()
    verified = BooleanField(default=False)
    location = DictField()
    status = StringField(default='ACTIVE', choices=('ACTIVE', 'SUSPENDED'))
    permissions = StringField()
    favoriteVendors = ListField(DynamicField())
    createdAt = DateTimeField(default=dt.now())
    updatedAt = DateTimeField(default=dt.now())
    v = IntField(db_field='__v')

    def __repr__(self):
        return '<User %r>' % (self.email)

    def toJson(self):
        return {
            '_id': self.pk,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'password': self.password,
            'email': self.email,
            'lastLogin': self.lastLogin,
            'dateOfBirth': self.dateOfBirth,
            'phone': self.phone,
            'resetPasswordToken': self.resetPasswordToken,
            'resetPasswordExpires': self.resetPasswordExpires,
            'role': self.role,
            'token': self.token,
            'imageUrl': self.imageUrl,
            'address': self.address,
            'cordinates': self.cordinates,
            'verified': self.verified,
            'location': self.location,
            'status': self.status,
            'permissions': self.permissions,
            'favoriteVendors': self.favoriteVendors,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            '__v': self.v,
        }