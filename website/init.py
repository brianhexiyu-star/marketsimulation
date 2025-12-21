from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
import os
import secrets

db = SQLAlchemy()
csrf = CSRFProtect()   # CSRF object

def create_app():
    app = Flask(__name__)

    # Secret key for session, use env variable if set (persistent across deploys)
    app.config['SECRET_KEY'] = "highly_secure_and_random_secret_key"  # replace with os.getenv("SECRET_KEY") in production

    # PostgreSQL connection, use DATABASE_URL env variable for Vercel/cloud
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://neondb_owner:npg_9SIyFxO5GVgv@ep-cool-cell-a15lc2ae-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Optional SQLite binds if you still need local testing for market items
    app.config['SQLALCHEMY_BINDS'] = {
        'market': 'sqlite:///market.db',
        'marketItem': 'sqlite:///market_item.db'
    }

    # Secure session cookies
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = bool(os.getenv("SESSION_COOKIE_SECURE", False))

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth
    from .market import market
    from .account import account
    from .premium import premium

    app.register_blueprint(premium)
    app.register_blueprint(account)
    app.register_blueprint(market)
    app.register_blueprint(views)
    app.register_blueprint(auth)

    # Create tables if they don't exist (Flask-Migrate recommended for production)
    with app.app_context():
        db.create_all()

    return app
