from .items.routes import items_bp
app.register_blueprint(items_bp, url_prefix='/api')
