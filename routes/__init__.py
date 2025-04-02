from flask import Flask

def register_blueprints(app: Flask):
    from .api import bp as api_bp
    app.register_blueprint(api_bp)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)
