from flask import Flask
from datetime import timedelta
from dotenv import load_dotenv
import os
from pymongo.errors import PyMongoError

from .extention import mongo, bcrypt, jwt
from .routes.product__route import product_bp
from .routes.auth__route import auth__bp

load_dotenv()  # Load .env variables

def create_app():
    app = Flask(__name__)

    # MongoDB config
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")
    mongo.init_app(app)
    try:
        mongo.cx.admin.command("ping")   # same as MongoDB health check
        app.logger.info("✅ MongoDB connected successfully")
        print("✅ MongoDB connected successfully")
    except PyMongoError as e:
        app.logger.error(f"❌ MongoDB connection failed: {e}")
        print(f"❌ MongoDB connection failed: {e}")

    bcrypt.init_app(app)

    # JWT config
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=int(os.getenv("JWT_EXPIRES_HOURS", 1))
    )

    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_HTTPONLY"] = True
    app.config["JWT_COOKIE_SAMESITE"] = "None"

    jwt.init_app(app)

    app.register_blueprint(product_bp, url_prefix="/api/product")
    app.register_blueprint(auth__bp, url_prefix="/api/auth")

    return app
