import os
from flask import Flask, render_template
from flask_cors import CORS
from googlemaps import Client

from fuudzie.JSONEncoder import JSONEncoder
from fuudzie.routes.cart import cartRoutes
from fuudzie.routes.geo import geoRoutes
from fuudzie.routes.payment import paymentRoutes
from fuudzie.test.rave import testRoutes
from fuudzie.routes.order import orderRoutes
from fuudzie.instances import initializeDB, initializeJWT, initializeMail
from fuudzie.admin import initializeAdmin
    


def create_app(test_config=None):
    # create and configure the app
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
   
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=False)
        #app.config.from_envvar('APP_CONFIG')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    '''change jsonify default JSON encoder to a custom Encode
    ### to support Model encoding for {users, vendors, carts, etc}
    '''
    app.json_encoder = JSONEncoder

    #initialize mongodb instance
    initializeDB(app)

    #initialize jwt
    initializeJWT(app)

    #initialize Admin
    initializeAdmin(app)

    #initialize Mail
    initializeMail(app)

    #app.json_encoder = MongoEngineJSONEncoder
    #register blueprint/routes
    app.register_blueprint(cartRoutes)
    app.register_blueprint(geoRoutes)
    app.register_blueprint(paymentRoutes)
    app.register_blueprint(orderRoutes)
    app.register_blueprint(testRoutes)

    #Enable cors for all routes/view
    CORS(app)

    #instatiate map 
    #initializeGoogleMap(app)
    with app.app_context():
        app.gmap = Client(key=app.config['GOOGLE_API_KEY'])

    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    @app.route('/email')
    def email_temp():
        return render_template('new-order.html', content={'name': 'Yam porage', 
                                'description': 'it just yam porage', 'pricePerOrderSize': 2000, 
                                'mealImages': ['https://media.gettyimages.com/photos/oatmeal-porridge-in-bowl-picture-id568138593?s=612x612'],
                                'quantity': 4, })

    

    return app