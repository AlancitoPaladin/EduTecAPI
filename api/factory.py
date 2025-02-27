from flask import Flask

from api.auth_routes import auth_bp
from database.mongo_config import init_db, mongo
from api.user_routes import user_bp


def create_app():
    app = Flask(__name__)

    init_db(app)  # ✅ Initialize MongoDB

    app.register_blueprint(user_bp)  # ✅ Register routes
    app.register_blueprint(auth_bp)

    return app
