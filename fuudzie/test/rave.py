from flask import Blueprint, request, jsonify
from bson.json_util import ObjectId

from fuudzie.models.Payment import FlutterWave
from fuudzie.util import validatePaymentDetails
from fuudzie.models.User import Users

testRoutes = Blueprint('test', __name__, url_prefix="/api/v2/test")

'''
# Fund wallet
'''
@testRoutes.route('/initiate-payment', methods=('GET','POST'))
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
                return jsonify(res), 200
        else:
            return jsonify({"status": "failed", 'msg': "Something happened cannot\
                            initiate payment please try again later",}), 400


    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500


@testRoutes.route('/enter-otp',methods=['GET','POST'])
def handleOTP():
    
    otp = None
    ref = None

    if request.method == 'POST':
        otp = request.json.get('otp')
        ref = request.json.get('ref')

    print(request.get_json())

    if otp == None or ref == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400

    rave = FlutterWave()

    res = rave.validatePayment(ref,otp)

    return jsonify(res), 200



@testRoutes.route('/verify-payment',methods=['GET','POST'])
def handleVerification():
    
    amount = None
    ref = None

    if request.method == 'POST':
        amount = request.json.get('amount')
        ref = request.json.get('ref')

    print(request.get_json())

    if ref == None or amount == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400

    rave = FlutterWave()

    verify = rave.verifyPayment(ref,amount)

    if verify == True:
        return jsonify({'msg': "amount charged match provided amount", 'status': 'success'}), 200
    else:
        return jsonify({'msg': "amount charged  does not match provided amount", 'status': 'success'}), 200

