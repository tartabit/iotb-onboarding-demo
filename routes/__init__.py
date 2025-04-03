from flask import Flask

def register_blueprints(app: Flask):
    from .api import bp as api_bp
    app.register_blueprint(api_bp)

    from .customer import bp as customer_bp
    app.register_blueprint(customer_bp)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .onboarding import bp as onboarding_bp
    app.register_blueprint(onboarding_bp)
