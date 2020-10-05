from flask import ( Blueprint, request, jsonify)
from bson.json_util import loads, dumps, ObjectId
import traceback


from fuudzie.models.Cart import Carts
from fuudzie.models.Meal import Meals, MealEmbedded
from fuudzie.models.Order import Orders
from fuudzie.models.Vendor import Vendors
from fuudzie.models.Escrow import Escrows
from fuudzie.email import NewOrderUserMail, NewOrderVendorMail
from fuudzie.util import makeCardPayment, makeRefund, payFromWallet, refundWallet, calculateDelvFee


orderRoutes = Blueprint('order', __name__, url_prefix='/api/v2/orders')

@orderRoutes.route('/create', methods=['POST'])
def createOrder():
    
    shippingAddr = None
    userId = None
    instructions = None
    ref = None


    # Check if method is POST and retrive body of request
    if request.method == 'POST':
        userId = ObjectId(request.json.get('userId'))
        shippingAddr = request.json.get('shippingAddress')
        instructions = request.json.get('instructions')
        ref = request.json.get('ref')
        
    

    if shippingAddr == None or userId == None or ref == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400


    #try:
    #get user cart
    cart = Carts.objects(user=userId).first()


    if cart :
        
        #if payment successful attempt creating order
        #Create user order from cart
        order = Orders(
            items = cart.cartItems,
            shippingAddress = shippingAddr,
            user = cart.user,
            amount = cart.totalPrice,
            deliveryFee = cart.deliveryFee,
            paymentId = ref,
            status ='paid'
        )
        order.save()

        #Notify vendors of new orders
        for item in order.items:
            vendor = Vendors.objects(pk=item.vendor.pk).first()
            escrow = Escrows.objects(vendor=vendor.pk, order=order.pk).first()

            if escrow:
                escrow.update(
                    inc__amount=item.pricePerOrderSize
                )
                escrow.save()
            else:
                escrow = Escrows(
                    amount=item.pricePerOrderSize,
                    vendor=vendor.pk,
                    order=order.pk,
                )

                escrow.save()

            

        for key in cart.feesPerVendor.keys():
            
            vendor = Vendors.objects(pk=ObjectId(key)).first()
            items = cart.cartItems.filter(businessName=vendor.businessName)
            
            email = vendor.user.email
            name = vendor.businessName
            instruction = ''
            sumTotal = 0
            for item in items:
                sumTotal = sumTotal + item.pricePerOrderSize
            if instructions != None:
                if vendor.businessName in instructions:
                    instruction = instructions[vendor.businessName]
            mail = NewOrderVendorMail(email, name, items, sumTotal, instruction)

            mail.create_mail()

        fullName = cart.user.firstName +' '+ cart.user.lastName
        items = cart.cartItems
        total = cart.totalPrice
        delvfee = cart.deliveryFee
        userMail = NewOrderUserMail(cart.user.email, fullName, items, total, delvfee)
        userMail.create_mail()
            

        # delete cart after creating order
        cart.delete()
            
        
        return jsonify({"status": "ok", "data": order, 'msg': 'Order successfully'}), 201

        

    #if cart is empty
    else:
        return jsonify({"status": "failed", 'msg': 'Cart not found'}), 404
    '''except Exception as e:
        print(e)
        return jsonify({"status": "failed",
                 "data": 'something happened cannot place order', 'msg': 'can not handle this request at the moment'}), 500'''



@orderRoutes.route('/view')
def viewAll():
    orders = [] 
    try:

        for row in Orders.objects():
            orders.append(row)

        if len(orders) <= 0:
            return jsonify({"status": "failed", "msg": "Nothing to see here",'data': []}), 404
                
        return jsonify({"status": "ok", 'msg': 'All Orders', "data": orders}), 200
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500


@orderRoutes.route('/vendor/<path>/list')
def get_vendor_order_list(path):

    try:
        orders = []

        vendor = Vendors.objects(user=ObjectId(path)).first()

        for row in Orders.objects(items__vendor=vendor.pk):
            orders.append(row)

        if len(orders) <= 0:
            return jsonify({"status": "failed", "msg": "Vendor order is Empty",'data': []}), 404
        
                
        return jsonify({"status": "ok", 'msg': 'All vendor orders', "data": orders}), 200
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500


@orderRoutes.route('/view/status/<path>')
def get_order_by_status(path):
    try:
        orders = []

        for row in Orders.objects(status=path):
            orders.append(row)

        if len(orders) <= 0:
            return jsonify({"status": "failed", "msg": "Vendor order is Empty", 'data': []}), 404
        
                
        return jsonify({"status": "ok", 'msg': 'All vendor orders', "data": orders}), 200
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500
    