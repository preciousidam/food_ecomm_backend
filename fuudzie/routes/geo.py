from flask import Blueprint, jsonify, request
from bson.json_util import loads, dumps, ObjectId

from fuudzie.util import getAddress, getCoordinates, calculateDelvFee
from fuudzie.models.Cart import Carts
from fuudzie.models.Order import Orders
from fuudzie.models.Meal import MealEmbedded, Meals
from fuudzie.models.AppSettings import Appsettings


geoRoutes = Blueprint('geo', __name__, url_prefix='/api/v2/geo')


@geoRoutes.route('/get-address-from-coord/', methods=['GET'])
def getAddressFromCoord():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if not (lat or lng):
        return jsonify({'msg': "incomplete params enter lat and lng", 'status': 'failed'})

   
    address = getAddress((lat,lng))
    return jsonify(address)
    

@geoRoutes.route('/get-coord-from-address/', methods=['GET'])
def getCoordFromAddress():
    address = request.args.get('address')

    if not address:
        return jsonify({'msg': "no address was provided", 'status': 'failed'})
   
    coord = getCoordinates(address)

    return jsonify(coord)

@geoRoutes.route('/delivery-fee/', methods=['GET'])
def getDevlFee():
    address = request.args.get('address')
    settings = Appsettings.objects().get()
    if address == None:
        return jsonify({"status": "failed", "msg": "Missing Address in request body"}), 400

    id = request.args.get('id')
    coord = getCoordinates(address)

    if coord:
        
        cart = Carts.objects(user=ObjectId(id)).first()
        
        if cart and not settings.deliveryPromo:
            if coord['lat'] == cart.deliveryLocation.get('latitude') and coord['lng'] == cart.deliveryLocation.get('longitude'):
                return jsonify({'data': {'deliveryFee': cart.deliveryFee, 'coord': coord, 'address': address}, 'msg': 'New delivery fee calculated', 'status': 'ok'}), 200

            cartItems = cart.cartItems
            totalDelvFee = 0
            deliveryFees = cart.feesPerVendor

            for item in cartItems:
                lat = item.vendor.cordinates['latitude']
                lng = item.vendor.cordinates['longitude']
                delPrice = calculateDelvFee((coord['lat'],coord['lng']),(lat,lng))
                totalDelvFee = totalDelvFee + delPrice
                deliveryFees.update({str(item.vendor.pk): delPrice})

            
            if totalDelvFee > 0:
                cart.update(
                    set__deliveryFee=totalDelvFee,
                    set__deliveryLocation= [address,{"latitude": coord['lat'], "longitude": coord['lng']}],
                    set__feesPerVendor=deliveryFees
                )
                
                cart.save()
                cart.reload()

                return jsonify({'data': {'deliveryFee': cart.deliveryFee, 'coord': coord, 'address': address}, 'msg': 'New delivery fee calculated', 'status': 'ok'}), 200
            
        
        else:
            return jsonify({'data':{'deliveryFee': cart.deliveryFee}, 'status': 'failed'}), 400
        
        


        
@geoRoutes.route('/change/')
def someRandomTask2():
    orders = None

    try:
        orders = Orders.objects()

        if orders:
            count = 1
            for order in orders:
               
                for item in order.items:
                    if not isinstance(item,MealEmbedded):
                        meal = Meals.objects(pk=item['item']).first()
                        
                        if meal:
                            
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
                                quantity = 1,
                                timeToPrepare = meal.timeToPrepare,
                            )
                            order.update(
                                add_to_set__items=mealEmbedded
                            )        

                    else:
                        print('mealEmbedded')
                        print(item)
                order.save()
                count = count + 1
        return 'done'
    except Exception as e:
        print(e)


@geoRoutes.route('/delete/')
def someRandomTask():
    orders = None

    try:
        orders = Orders.objects()

        if orders:
            count = 1
            for order in orders:
                print(count)
                for item in order.items:
                    if not isinstance(item,MealEmbedded):
                        print('deleting non instance of mealembedded')
                        order.update(
                            pull__items__item=item['item']
                        )
                        
                    else:
                        print('mealEmbedded')
                        print(item)
                order.save()
                count = count + 1
        return 'done'
    except Exception as e:
        print(e)