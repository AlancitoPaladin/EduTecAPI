from flask import Blueprint, request, jsonify
from bson import ObjectId
from database import mongo_config
from models.user_models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"data": None}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user_collection = mongo.db.users

    user = user_collection.find_one({"email": email})
    if not user and check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password"}), 401
    else:
        return jsonify({"message": "Login successful"}), 200


@auth_bp.route('/logout', methods=["POST"])
def logout():
    pass


@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    email = data.get['email']
    password = data.get['password']
    user_collection = mongo.db.users

    if user_collection.find_one({'email': email}):
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = generate_password_hash(password)

    user = {
        'firstName': data.get['firstName'],
        'lastName': data.get['lastName'],
        'middleName': data.get['middleName'],
        'email': email,
        'password': hashed_password,
        'role': data.get['role'],
    }

    return jsonify({"message": "Usuario registrado"}), 201
