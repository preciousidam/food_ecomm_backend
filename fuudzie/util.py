from flask import current_app as app, jsonify, request
from json import loads
import math


from fuudzie.models.Payment import FlutterWave
from fuudzie.models.User import Users
from fuudzie.models.Wallet import Wallets
from fuudzie.models.Transaction import Transactions


def calculateDelvFee(frm, to):
    try:
        result = app.gmap.distance_matrix(frm,to)
        dist = result.get('rows')[0].get('elements')[0].get('distance').get('value') / 1000
        durtn = result.get('rows')[0].get('elements')[0].get('duration').get('value') / 60
        return math.ceil((dist * 65) + (durtn * 5) + 200)
    except Exception as e:
        print(e)
        return 1000

def getCoordinates(address):
    try:
        coordinates = app.gmap.geocode(address)
        
        lat = coordinates[0].get("geometry").get("location").get("lat")
        lng = coordinates[0].get("geometry").get("location").get("lng")
        return {'status': 'ok', 'lat': lat, 'lng': lng}
    except Exception as e:
        print(e)
        return {'status': 'failed', 'msg': e}

def getAddress(coordinates):
    try:
        coordinates = app.gmap.reverse_geocode(coordinates)
        return {'address': coordinates[0].get("formatted_address"), 'status': 'ok'}
    except Exception as e:
        print(e)
        return {'status': 'failed', 'msg': e}


def validatePaymentDetails(details):

    error = {'status': 'ok', 'msg': ''}
    msg = ''

    try:
        if not details.get('cardno'):
            return error.update({'msg': msg+'Card number not provided ', 'status': 'bad'})
        
        if not details.get('cvv'):
            return error.update({'msg': msg+'cvv number not provided ', 'status': 'bad'})

        if not details.get('pin'):
            return error.update({'msg': msg+'pin number not provided ', 'status': 'bad'})
            
        if not details.get('expirymonth'):
            return error.update({'msg': msg+'expiry month not provided ', 'status': 'bad'})

        #if not details.get('amount'):
            #return error.update({'msg': msg+'amount not provided ', 'status': 'bad'})
            
        if not details.get('expiryyear'):
            return error.update({'msg': msg+'expiry year not provided ', 'status': 'bad'})

        if not details.get('userId'):
            return error.update({'msg': msg+'user Id not provided ', 'status': 'bad'})


        if 'amount' in details:
            
            if not details.get('amount'):
                return error.update({'msg': msg+'amount not provided ', 'status': 'bad'})
            
        
        return error
    except Exception as e:
        print(e)

def makeCardPayment(data, amount):
    
    error = validatePaymentDetails(data)
    
    if error['status'] == 'bad':
        return jsonify(error), 400

    cardno = data['cardno']
    cvv = data['cvv']
    pin = data['pin']
    amount = amount
    userId = data['userId']
    expiryyear = data['expiryyear']
    expirymonth = data['expirymonth']

    
    try:
        user = Users.objects(pk=userId).first()
        rave = FlutterWave(cardno, cvv, expirymonth, expiryyear, pin, amount, user)

        res = rave.pay_via_card()

        return res
    except Exception as e:
        print(e)
        return {"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}

def makeRefund(ref):

    rave = FlutterWave()
    
    response = rave.refund(ref)

    return response


def payFromWallet(userId, amount):

    try:
        wallet = Wallets.objects(user=userId).first()
        if wallet.amount >= amount:
            wallet.update(inc__amount=(amount * -1))
            wallet.save()
            wallet.reload()

            transaction = Transactions(
                user=wallet.user,
                wallet=wallet.pk,
                amount=amount,
                reference='WAL-'+str(wallet.pk),
                operation="deposit"
            )
            transaction.save()

            return {'status': 'ok', 'ref': 'WAL-'+str(wallet.pk), 'msg': "Payment successful"}
        else:
            return {'status': 'failed', 'msg': 'Insufficient funds'}
    except Exception as e:
        print(e)
        return {'status': 'failed'}



def refundWallet(userId, amount):

    try:
        wallet = Wallets.objects(user=userId)
        wallet.update(inc__amount=amount)
        wallet.save()
        wallet.reload()

        return {'status': 'success', 'data': {'flwRef': 'WAL-'+str(wallet.pk)}}
    except Exception as e:
        print(e)
        return {'status': 'failed'}

