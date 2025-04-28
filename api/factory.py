from flask import Flask
from database.mongo_config import init_db, mongo
from api.auth_routes import auth_bp
from api.user_routes import user_bp
from api.teacher_routes import teacher_bp


def create_app():
    app = Flask(__name__)

    init_db(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(teacher_bp)

    return app
