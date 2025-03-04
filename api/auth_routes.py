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
        return jsonify({"message": "Se requieren el email y contraseña"}), 400

    user_collection = mongo.db.users

    user = user_collection.find_one({"email": email})
    if not user and check_password_hash(user["password"], password):
        return jsonify({"message": "Correo o contraseña inválida"}), 401
    else:
        return jsonify({"message": "Ingreso completado"}), 200


@auth_bp.route('/logout', methods=["POST"])
def logout():
    pass


@auth_bp.route('/register', methods=["POST"])
def register():
    name = data.get('name')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not name or not last_name or not email or not password or not role:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    user_collection = mongo.db.users

    if user_collection.find_one({'email': email}):
        return jsonify({"error": "Correo ya registrado"}), 409

    hashed_password = generate_password_hash(password)

    user = {
        'name': name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password,
        'role': role
    }

    user_collection.insert_one(user)

    return jsonify({"message": "Usuario registrado"}), 201
