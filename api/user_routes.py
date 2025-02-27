from flask import Blueprint, request, jsonify
from bson import ObjectId
from database import mongo_config

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/courses', methods=["GET"])
def courses():
    Courses = [
        {"Course": "Ingeniería de Software", "Duration": "Feb-Junio 2025", "Teacher": "Alan Carlos Hernández",
         "Image": "https://miro.medium.com/v2/resize:fit:4800/format:webp/1*gQzkQ3uJ0SwJL51t16bivw.jpeg",
         "Stars": 4.9},
        {"Course": "Desarrollo de aplicaciones móviles", "Duration": "Feb-Junio 2025", "Teacher": "Luis Vázquez",
         "Image": "https://cms.rootstack.com/sites/default/files/inline-images/Captura%20de%20pantalla%202024-01-11%20a%20la%28s%29%2014.33.17.jpg",
         "Stars": 4.7},
        {"Course": "Desarrollo de backend", "Duration": "Julio-Diciembre 2025", "Teacher": "Mario García",
         "Image": "https://www.azulschool.net/wp-content/uploads/2020/05/Databasse-Administrator-1024x709.jpg",
         "Stars": 4.4}
    ]
    return jsonify(Courses)
