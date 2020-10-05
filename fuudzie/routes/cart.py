from flask import ( Blueprint, request, jsonify)
from bson.json_util import loads, dumps, ObjectId
import traceback


from fuudzie.models.Cart import Carts
from fuudzie.models.Meal import Meals, MealEmbedded
from fuudzie.models.AppSettings import Appsettings
from fuudzie.util import calculateDelvFee


cartRoutes = Blueprint('cart', __name__, url_prefix='/api/v2/cart')


@cartRoutes.route('/create/<path>', methods=['POST'])
def addToCart(path):
    userId = None
    mealId = None
    qty = 1
    latitude = None
    longitude = None
    cart = None
    address = None
    settings = Appsettings.objects().get()

    # Check if method is POST and retrive body of request
    if request.method == 'POST':
        userId = request.json.get('userId')
        mealId = request.json.get('mealId')
        latitude = request.json.get('latitude')
        longitude = request.json.get('longitude')
        address = request.json.get('address')
        
    
    # Check for missing fields and return error if any
    if userId == None or  mealId == None or latitude == None or longitude == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400


    # create cart and insert meal
    try:

        # get meal if it exits
        meal = Meals.objects(pk=ObjectId(mealId)).first()

        # get user cart if it exist
        cart = Carts.objects(user=ObjectId(userId)).first()

        # calculate delivery fee
        delPrice = 0 if settings.deliveryPromo == True else calculateDelvFee((meal.cordinates.get('latitude'),meal.cordinates.get('longitude')),(latitude,longitude))

        
        mealEmbedded = MealEmbedded(
            _id = str(meal.pk),
            vendor = meal.vendor,
            name = meal.name,
            description = meal.description,
            orderType = meal.orderType,
            orderSize = meal.orderSize,
            pricePerOrderSize = meal.pricePerOrderSize,
            cordinates = meal.cordinates,
            businessName = meal.businessName,
            businessLocation = meal.businessLocation,
            mealImages = meal.mealImages,
            quantity = qty,
            timeToPrepare = meal.timeToPrepare,
        )

        if cart != None:
            
            # check if meal already in cart
            exist = cart.cartItems.filter(name=meal.name).count()

            # if meal not in cart create and add meal
            if exist <= 0:
                
                deliverFees = { str(mealEmbedded.vendor.pk): delPrice}
                for key in cart.feesPerVendor:
                    deliverFees.update({key: cart.feesPerVendor.get(key)})
                
                totalDelvFee = sum(deliverFees.values())

                cart.update(
                    add_to_set__cartItems=mealEmbedded, 
                    inc__totalQuantity=1,
                    set__totalPrice= cart.totalPrice + (meal.pricePerOrderSize * float(qty)),
                    set__deliveryFee=totalDelvFee,
                    set__feesPerVendor= deliverFees
                )
                cart.save()
                cart.reload()

            # if meal already in cart update quantity
            else:
                return jsonify({'status': 'ok', 'data': cart, 'msg': 'Item already exist in cart'})
        
        # if cart for user is empty create one and add meal
        else:

            deliverFees = { str(mealEmbedded.vendor.pk): delPrice }

            # create cart and add meal
            cart = Carts(
                user = ObjectId(userId),
                cartItems = [mealEmbedded],
                totalQuantity = 1,
                totalPrice = meal.pricePerOrderSize * mealEmbedded.quantity,
                status = 'open',
                deliveryFee=delPrice,
                fixedFee = False,
                deliveryLocation = {"latitude": latitude, "longitude": longitude},
                feesPerVendor= deliverFees
            )
            cart.save()
            
                
        return jsonify({"status": "ok", "data":cart, 'msg': 'item added to cart successfully'}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500


@cartRoutes.route('/update/<path>', methods=['POST'])
def updateCartItem(path):
    userId = None
    mealId = None
    qty = None

    if request.method == 'POST':
        userId = request.json.get('userId')
        mealId = request.json.get('mealId')
        qty = request.json.get('qty')


    if userId == None or  mealId == None or qty == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400

    try:
        # get user cart if it exist
        cart = Carts.objects(user=ObjectId(userId)).first()

        if cart != None:
            totalPrice = cart.totalPrice
            oldQty = cart.cartItems.get(_id=mealId).quantity
            pricePerItem = cart.cartItems.get(_id=mealId).pricePerOrderSize

            cart.totalPrice = totalPrice - (float(oldQty) * pricePerItem)
            cart.save()
            cart.reload()
            
            cart.cartItems.get(_id=mealId).quantity = qty
            
            cart.totalPrice = cart.totalPrice + (float(qty) * pricePerItem)
            cart.save()
            cart.reload()
            
        return jsonify({"status": "ok", "data": cart, 'msg': 'cart item updated'}), 201
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500


'''
# delete from cart function
# take userId and mealId
'''
@cartRoutes.route('/delete', methods=['POST'])
def deleteFromCart():
    userId = None
    mealId = None
    qty = None
    msg = ""
    latitude = None
    longitude = None
    settings = Appsettings.objects().get()


    if request.method == 'POST':
        userId = request.json.get('userId')
        mealId = ObjectId(request.json.get('mealId'))
        qty = request.json.get('qty')
        latitude = request.json.get('latitude')
        longitude = request.json.get('longitude')
    

    if userId == None or  mealId == None or qty == None:
        return jsonify({"status": "failed", "msg": "Bad request some fields are missing from request body"}), 400

    try:
        # get meal if it exists
        meal = Meals.objects(pk=ObjectId(mealId)).first()

        # get user cart if it exists
        cart = Carts.objects(user=ObjectId(userId)).first()

        # if cart not empty
        if cart != None:

            # delete meal from cart
            # update cart
            cart.update(
                pull__cartItems___id=str(mealId),
                inc__totalQuantity=-1,
                inc__totalPrice= (meal.pricePerOrderSize * float(-1 * qty))
            )
            cart.save()
            cart.reload()

            # check if vendor still has at list one item meal already in cart
            # else substract delivery fee from total
            exist = cart.cartItems.filter(businessName=meal.businessName).count()   
            
            if exist <= 0:
                delPrice = 0 if settings.deliveryPromo == True else cart.feesPerVendor.get(str(meal.vendor.pk))
                cart.update(
                    inc__deliveryFee=(delPrice * -1)
                )

                cart.save()
                cart.reload()


            # Delete Cart if empty
            if cart.cartItems.count() == 0:
                cart.delete()
                msg = "Cart is empty"
                return jsonify({"status": "ok", "msg":msg, "data": {}}), 201

            msg = "Item removed from cart" 
            return jsonify({"status": "ok", "msg":msg, "data": cart}), 201

        else:
            msg = "Cart is empty"
            return jsonify({"status": "ok", "msg":msg, "data": {}}), 201
                
        
        
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500


@cartRoutes.route('/view')
def viewCart():
    carts = [] 
    try:

        for row in Carts.objects():
            carts.append(row)

        if len(carts) <= 0:
            return jsonify({"status": "failed", "msg": "Cart is Empty", "data": {}}), 404
                
        return jsonify({"status": "ok", 'msg': 'All cart items', "data": carts}), 200
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500


@cartRoutes.route('/view/<path>')
def userCart(path):

    try:
        
        cart = Carts.objects(user=ObjectId(path)).first()

        if not cart:
            return jsonify({"status": "failed", "msg": "Cart is Empty", "data": {}}), 404
    
              
        return jsonify({"status": "ok",'msg': 'All cart items', "data": cart}), 200
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "msg": "something happened server cannot  \
            handle this request at the moment try again later"}), 500

