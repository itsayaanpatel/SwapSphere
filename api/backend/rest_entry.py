from flask import Flask

from backend.db_connection import db
from backend.customers.customer_routes import customers
from backend.products.products_routes import products
from backend.simple.simple_routes import simple_routes
import os
from dotenv import load_dotenv


# simple routes
from backend.simple.simple_routes import simple_routes

# customer & product
from backend.customers.customer_routes     import customers
from backend.products.products_routes      import products

# buyer & seller
from backend.buyers.buyer_routes           import buyer
from backend.sellers.seller_routes         import seller

# item routes (in item_routes folder)
from backend.items.item_routes             import items

# trades
from backend.trades.trade_routes           import trades

# admin (users, fraud, logs, analytics, ML)
from backend.admin.admin_routes            import admin_bp
from backend.analytics.analytics_routes    import analytics

# market valuations
from backend.products.market_valuations    import market_valuations

# negotiate deals
from backend.buyers.buyer_negotiation       import negotiation
from backend.cash_deals                     import cash_deals
#from backend.trade_negotiation              import trade_negotiation



def create_app():
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(simple_routes)
    app.register_blueprint(customers,   url_prefix='/')
    app.register_blueprint(products,    url_prefix='/')
    app.register_blueprint(buyer,       url_prefix='/')
    app.register_blueprint(market_valuations, url_prefix='/')
    app.register_blueprint(seller,      url_prefix='/')
    app.register_blueprint(items,       url_prefix='/')
    app.register_blueprint(trades,      url_prefix='/')
    app.register_blueprint(cash_deals,      url_prefix='/')
    app.register_blueprint(analytics,   url_prefix='/')
    app.register_blueprint(admin_bp,    url_prefix='/')
    app.register_blueprint(negotiation, url_prefix='/')
    #app.register_blueprint(trade_negotiation, url_prefix='/')

    # Don't forget to return the app object
    return app

