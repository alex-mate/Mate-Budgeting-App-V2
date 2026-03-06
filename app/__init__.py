from flask import Flask
from app.config import Config
from app.extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app import models  # important for migrations

    # Register blueprints HERE (inside function)
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.accounts import accounts_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(accounts_bp)

    return app


from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))