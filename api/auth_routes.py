from flask import Blueprint, request, jsonify
from bson import ObjectId
from database.mongo_config import mongo
from models.user_models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from api.utils import send_password, send_notification

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
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Correo o contraseña inválida"}), 401
    else:
        return jsonify({"message": "Ingreso completado"}), 200


@auth_bp.route('/logout', methods=["POST"])
def logout():
    pass


@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibieron datos en formato JSON"}), 400

    name = data.get('name')
    last_name = data.get('last_name')
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


@auth_bp.route('/reset_password', methods=["POST"])
def reset_password():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    user_collection = mongo.db.users

    if user_collection.find_one({'email': data['email']}):

        new_password = "NuevoPassword"  # Replace with actual password generation logic

        # Update the user's password in the database
        user_collection.update_one(
            {'email': data['email']},
            {'$set': {'password': generate_password_hash(new_password)}}
        )# Hacer una consulta de actualización donde encontrar el email, generar una nueva contraseña
        # Remplazar la contraseña generada
        send_password(data['email'], new_password) # Pasar como argumentos el correo y la contraseña generada para enviarla al usuario
        return jsonify({"message": "Correo realizado"}), 200


@auth_bp.route('/notifications', methods=["POST"])
def notifications():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    user_collection = mongo.db.users

    if user_collection.find_one({'email': data['email']}):
        send_notification()
        return jsonify({"message": "Correo realizado"}), 200

