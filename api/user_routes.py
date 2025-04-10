from flask import Blueprint, request, jsonify
from database.mongo_config import mongo
from bson import ObjectId
from bson.errors import InvalidId

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/courses', methods=["GET"])
def courses():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    courses_collection = mongo.db.courses

    projection = {
        "_id": 1,
        "course": 1,
        "image": 1,
        "stars": 1,
        "description": 1
    }

    try:
        courses_cursor = courses_collection.find({}, projection) \
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


@user_bp.route('/course/<id>', methods=["POST"])
def course(id):
    try:
        if not ObjectId.is_valid(id):
            return jsonify({"message": "Invalid course ID"}), 400

        course = mongo.db.courses.find_one({"_id": ObjectId(id)})
        if not course:
            return jsonify({"message": "Course not found"}), 404

        course["_id"] = str(course["_id"])
        return jsonify(course), 200

    except InvalidId:
        return jsonify({"message": "Invalid course ID format"}), 400
    except Exception as e:
        return jsonify({"message": "Ocurrió un error", "error": str(e)}), 500


@user_bp.route('/insert_course', methods=["GET"])
def insert_course():
    pass


@user_bp.route('/update_info', methods=["POST"])
def update_info():
    pass
