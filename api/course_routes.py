from flask import Blueprint, request, jsonify, send_file
from database.mongo_config import mongo
from models.course_models import Course, Announcement, Assignment  # Tus modelos Pydantic
from datetime import datetime, UTC
from bson import ObjectId
from bson.errors import InvalidId
import gridfs
from io import BytesIO

course_routes = Blueprint('course_routes', __name__)


@course_routes.route('/upload/<course_id>', methods=['POST'])
def upload_file(course_id):
    if 'file' not in request.files:
        return jsonify({'message': 'No se encontró archivo'}), 400

    fs = gridfs.GridFS(mongo.db)
    file = request.files['file']
    file_id = fs.put(file.stream, filename=file.filename, content_type=file.content_type, course_id=course_id)

    return jsonify({'message': 'Archivo subido correctamente', 'file_id': str(file_id)}), 201


@course_routes.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    fs = gridfs.GridFS(mongo.db)
    try:
        file = fs.get(ObjectId(file_id))
        return send_file(BytesIO(file.read()), download_name=file.filename, mimetype=file.content_type)
    except:
        return jsonify({'message': 'Archivo no encontrado'}), 404


@course_routes.route('/courses/<course_id>/announcements', methods=['POST'])
def create_announcement(course_id):
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': 'Título y contenido son obligatorios'}), 400

    try:
        course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
    except (InvalidId, TypeError):
        return jsonify({'message': 'ID de curso inválido'}), 400

    if not course:
        return jsonify({'message': 'Curso no encontrado'}), 404

    announcement_data = {
        "course_id": course_id,
        "title": title,
        "content": content,
        "created_at": datetime.now(UTC)
    }

    mongo.db.announcements.insert_one(announcement_data)

    return jsonify({'message': 'Anuncio creado exitosamente'}), 201


@course_routes.route('/courses/<course_id>/assignments', methods=['POST'])
def create_assignment(course_id):
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')  # Se espera en formato ISO

    if not title or not description or not due_date:
        return jsonify({'message': 'Título, descripción y fecha de entrega son obligatorios'}), 400

    try:
        course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
    except (InvalidId, TypeError):
        return jsonify({'message': 'ID de curso inválido'}), 400

    if not course:
        return jsonify({'message': 'Curso no encontrado'}), 404

    try:
        due_date_parsed = datetime.fromisoformat(due_date)
    except ValueError:
        return jsonify({'message': 'Formato de fecha inválido, usa ISO 8601'}), 400

    assignment_data = {
        "course_id": course_id,
        "title": title,
        "description": description,
        "due_date": due_date_parsed,
        "created_at": datetime.now(UTC)
    }

    mongo.db.assignments.insert_one(assignment_data)

    return jsonify({'message': 'Tarea asignada exitosamente'}), 201


@course_routes.route('/courses/<course_id>/content', methods=['POST'])
def get_course_content(course_id):
    try:
        ObjectId(course_id)
    except (InvalidId, TypeError):
        return jsonify({'message': 'ID de curso inválido'}), 400

    course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
    if not course:
        return jsonify({'message': 'Curso no encontrado'}), 404

    announcements = list(mongo.db.announcements.find({'course_id': course_id}))
    announcements_response = [{
        'id': str(a['_id']),
        'title': a['title'],
        'content': a['content'],
        'created_at': a['created_at'].isoformat() if 'created_at' in a else None
    } for a in announcements]

    assignments = list(mongo.db.assignments.find({'course_id': course_id}))
    assignments_response = [{
        'id': str(a['_id']),
        'title': a['title'],
        'description': a['description'],
        'due_date': a.get('due_date').isoformat() if a.get('due_date') else None
    } for a in assignments]

    materials = list(mongo.db.materials.find({'course_id': course_id}))
    materials_response = [{
        'id': str(m['_id']),
        'name': m['name'],
        'file_url': m.get('file_url', '')
    } for m in materials]

    return jsonify({
        'announcements': announcements_response,
        'assignments': assignments_response,
        'materials': materials_response
    }), 200
