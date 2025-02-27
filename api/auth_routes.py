from flask import Blueprint, request, jsonify
from bson import ObjectId
from database import mongo_config
from models.user_models import UserModel

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/login', methods=["POST"])
def login():
    pass

@auth_bp.route('/logout', methods=["POST"])
def logout():
    pass

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    email = data.get['email']
    password = data.get['password']

    collection = mongo.db.myCollection

    pass