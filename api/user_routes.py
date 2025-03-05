from flask import Blueprint, request, jsonify
from database.mongo_config import mongo
from bson import ObjectId

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/courses', methods=["GET"])
def courses():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    courses_collection = mongo.db.courses

    try:
        courses_cursor = courses_collection.find() \
            .skip((page - 1) * per_page) \
            .limit(per_page)
        courses_list = []

        for course in courses_cursor:
            course["_id"] = str(course["_id"])
            courses_list.append(course)

        return jsonify({
            "courses": courses_list,
            "page": page,
            "per_page": per_page,
        }), 200

    except Exception as e:
        return jsonify({"message": "Ocurrió un error", "error": str(e)}), 500


@user_bp.route('/insert_course', methods=["GET"])
def insert_course():
    pass

@user_bp.route('/update_info', methods=["POST"])
def update_info():
    pass
