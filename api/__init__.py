from flask import app
from .items.routes import items_bp
app.register_blueprint(items_bp, url_prefix='/api')
from .trades.routes import trades_bp
app.register_blueprint(trades_bp, url_prefix='/api')