from flask import Blueprint, jsonify, request
from bson.json_util import ObjectId

from fuudzie.models.Payment import FlutterWave
from fuudzie.util import validatePaymentDetails, payFromWallet, refundWallet
from fuudzie.models.User import Users
from fuudzie.models.Wallet import Wallets
from fuudzie.models.Transaction import Transactions


paymentRoutes = Blueprint('payments', __name__,url_prefix='/api/v2/payments')

'''
# Fund wallet
'''
@paymentRoutes.route('/rave/card', methods=('GET','POST'))
def makePayment():
    data = None
    if request.method == 'POST':
        data = request.get_json()
    print(request.get_json())
    error = validatePaymentDetails(data)
    print(error)
    if error['status'] == 'bad':
        return jsonify(error), 400

    cardno = data['cardno']
    cvv = data['cvv']
    pin = data['pin']
    amount = data['amount']
    userId = ObjectId(data['userId'])
    expiryyear = data['expiryyear']
    expirymonth = data['expirymonth']

    
    try:
        user = Users.objects(pk=userId).first()
        rave = FlutterWave(cardno, cvv, expirymonth, expiryyear, pin, amount, user)
        wallet = None

        res = rave.pay_via_card()

        if res['status'] == 'success':
            if res['data']["chargeResponseCode"] == "02":
                return jsonify({"status": "ok", 'msg': res['data']["chargeResponseMessage"],
                                'ref': res['data']["flwRef"]}), 200
        else:
            return jsonify({"status": "failed", 'msg': "Something happened cannot\
                            initiate payment please try again later",}), 400


    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500


@paymentRoutes.route('/rave/OTP',methods=['GET','POST'])
def handleOTP():
    
    otp = None
    ref = None
    amount = None
    userId = None
    wallet = None

    if request.method == 'POST':
        otp = request.json.get('otp')
        ref = request.json.get('ref')
        userId = request.json.get('userId')
        amount = request.json.get('amount')
    print(request.get_json())
    if otp == None or ref == None or userId == None or amount == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400

    rave = FlutterWave()

    res = rave.validatePayment(ref,otp)

    if 'data' in res['data'] and res['status'] == "success" and res['data']['data']['responsecode'] == '00':
        verify = rave.verifyPayment(res['data']['tx']['txRef'],amount)

        if verify:
            try:
                wallet = Wallets.objects(user=userId).first()

                if wallet:
                    wallet.update(
                        inc__amount=amount,
                        set__paymentRef=res['data']['data']['transactionreference']
                    )
                    wallet.save()
                    wallet.reload()
                else:
                    wallet = Wallets(user=userId, paymentRef=res['data']['data']['transactionreference'], amount=amount)
                    wallet.save()
                    wallet.reload()

                transaction = Transactions(
                    user=wallet.user,
                    wallet=wallet.pk,
                    amount=amount,
                    reference=wallet.paymentRef,
                    operation="deposit"
                )
                transaction.save()

                return jsonify({"status": "ok", "wallet": wallet, 'msg': 'Wallet funded successfully'}), 201
            except Exception as e:
                print(e)
                res = rave.refund(ref)
                return jsonify({"status": "failed", "wallet": wallet, 'msg': 'something happened cannot fund wallet'}), 500
        else:
            return jsonify({"status": "failed", "wallet": wallet, 'msg': 'Charge amount does not match enter amount'}), 402

    else:
        return jsonify({"status": "failed", "wallet": wallet, 'msg': res['data']['data']['responsemessage']}), 402


@paymentRoutes.route('/rave/checkout/OTP',methods=['GET','POST'])
def handlePaymentOTP():
    
    otp = None
    ref = None
    amount = None
    userId = None
    wallet = None

    if request.method == 'POST':
        otp = request.json.get('otp')
        ref = request.json.get('ref')
        userId = request.json.get('userId')
        amount = request.json.get('amount')
    print(request.get_json())
    if otp == None or ref == None or userId == None or amount == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400

    rave = FlutterWave()

    res = rave.validatePayment(ref,otp)

    if  'data' in res['data'] and res['status'] == "success" and res['data']['data']['responsecode'] == '00':
        verify = rave.verifyPayment(res['data']['tx']['txRef'],amount)

        if verify == True:
            try:
                wallet = Wallets.objects(user=userId).first()

                transaction = Transactions(
                    user=wallet.user,
                    wallet=wallet.pk,
                    amount=amount,
                    reference=ref,
                    operation="card Payment"
                )
                transaction.save()

                return jsonify({"status": "ok", "wallet": wallet, 'msg': 'Payment successful'}), 201
            except Exception as e:
                print(e)
                res = rave.refund(ref)
                return jsonify({"status": "failed", "wallet": wallet, 'msg': 'something happened cannot make payment'}), 500
        else:
            return jsonify({"status": "failed", "wallet": wallet, 'msg': 'Charge amount does not match enter amount'}), 402

    else:
        return jsonify({"status": "failed", "wallet": wallet, 'msg': res['data']['data']['responsemessage']}), 402


@paymentRoutes.route('/wallet/pay', methods=['GET', "POST"])
def payWithWallet():
    userId = None
    amount = None

    if(request.method == "POST"):
        userId = request.json.get('userId')
        amount = request.json.get('amount')

    if  userId == None or amount == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400

    res = payFromWallet(ObjectId(userId), amount)

    if res['status'] == 'ok':
        return jsonify(res), 201
    else:
        return jsonify(res), 402