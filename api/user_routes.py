from flask import Blueprint, request, jsonify
from database.mongo_config import mongo
from bson import ObjectId
from datetime import datetime
from bson.errors import InvalidId

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/update_info', methods=["POST"])
def update_info():
    pass


@user_bp.route('/add_course_student', methods=["POST"])
def add_course_student():
    data = request.get_json()
    course_id = data.get('courseId')
    student_email = data.get('studentEmail')
    state = data.get('state', True)

    if not course_id or not student_email:
        return jsonify({"message": "Falta courseId o studentEmail"}), 400

    if not ObjectId.is_valid(course_id):
        return jsonify({"message": "El courseId es inválido"}), 400

    enrollments = mongo.db.enrollments

    try:
        existing = enrollments.find_one({
            "courseId": ObjectId(course_id),
            "studentEmail": student_email
        })
        if existing:
            return jsonify({"message": "El alumno ya está inscrito en este curso"}), 400

        enrollment = {
            "courseId": ObjectId(course_id),
            "studentEmail": student_email,
            "state": state,
            "enrolledAt": datetime.utcnow()
        }
        enrollment_id = enrollments.insert_one(enrollment).inserted_id
        enrollment["_id"] = str(enrollment_id)

        return jsonify({
            "message": "Inscripción exitosa",
            "enrollment": enrollment
        }), 201

    except Exception as e:
        return jsonify({"message": "Error al inscribir", "error": str(e)}), 500


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


@user_bp.route('/get_courses_by_student', methods=["POST"])
def get_courses_by_student():
    data = request.get_json()
    user_email = data.get('userEmail')

    if not user_email:
        return jsonify({"error": "userEmail is required"}), 400

    try:
        enrollments = list(mongo.db.enrollments.find({"studentEmail": user_email}))

        course_ids = [enrollment["courseId"] for enrollment in enrollments]
        course_object_ids = [ObjectId(cid) for cid in course_ids if ObjectId.is_valid(cid)]

        projection = {
            "_id": 1,
            "course": 1,
            "image": 1,
            "stars": 1,
            "description": 1
        }

        courses_cursor = mongo.db.courses.find(
            {"_id": {"$in": course_object_ids}}, projection
        )

        courses = []
        for course in courses_cursor:
            course['_id'] = str(course['_id'])
            courses.append(course)
        return jsonify(courses), 200

    except Exception as e:
        return jsonify({"message": "Ocurrió un error", "error": str(e)}), 500


@user_bp.route('/news', methods=["GET"])
def news():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    courses_collection = mongo.db.courses

    projection = {
        "_id": 1,
        "course": 1,
        "image": 1,
        "stars": 1,
        "description": 1
    }

    try:
        latest_courses_cursor = courses_collection.find({}, projection) \
            .sort("_id", -1) \
            .skip((page - 1) * per_page) \
            .limit(per_page)

        latest_courses = []
        for course in latest_courses_cursor:
            course["_id"] = str(course["_id"])
            latest_courses.append(course)

        return jsonify({
            "courses": latest_courses,
            "page": page,
            "per_page": per_page
        }), 200

    except Exception as e:
        return jsonify({"message": "Ocurrió un error", "error": str(e)}), 500
