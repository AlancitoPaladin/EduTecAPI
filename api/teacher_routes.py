from flask import Blueprint, request, jsonify
from database.mongo_config import mongo
from bson import ObjectId
from bson.errors import InvalidId
from models.course_models import CourseModel
from datetime import datetime
from pytz import UTC
from pydantic import ValidationError

teacher_bp = Blueprint("teacher_bp", __name__)


@teacher_bp.route('/create_course', methods=["POST"])
def create_course():
    try:
        data = request.get_json()
        course = CourseModel(**data)
        course_dict = course.model_dump()

        result = mongo.db.courses.insert_one(course_dict)
        course_dict["_id"] = str(result.inserted_id)

        return jsonify({
            "message": "Curso creado exitosamente",
            "course": course_dict
        }), 201

    except ValidationError as e:
        return jsonify({
            "message": "Error de validación",
            "errors": e.errors()
        }), 400

    except Exception as e:
        return jsonify({
            "message": "Error al crear el curso",
            "error": str(e)
        }), 500


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
