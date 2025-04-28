from flask import Blueprint, request, jsonify
from database.mongo_config import mongo
from bson import ObjectId
from bson.errors import InvalidId

teacher_bp = Blueprint("teacher_bp", __name__)


@teacher_bp.route('/get_courses_by_teacher', methods=["POST"])
def get_courses_by_teacher():
    data = request.get_json()
    teacher_email = data.get('teacherEmail')

    if not teacher_email:
        return jsonify({"error": "teacherEmail is required"}), 400

    courses = list(mongo.db.courses.find({"teacherEmail": teacher_email}))

    for course in courses:
        course['_id'] = str(course['_id'])

    return jsonify(courses), 200
