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
    Courses = [
        # Ingenieria
        {
            "course": "Ingeniería de Software",
            "start": "Febrero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "alancarlos032104@gmail.com",
            "image": "https://miro.medium.com/v2/resize:fit:4800/format:webp/1*gQzkQ3uJ0SwJL51t16bivw.jpeg",
            "stars": 4.9,
            "category": "Ingeniería",
            "description": "Curso avanzado sobre desarrollo de software con metodologías ágiles y buenas prácticas.",
            "level": "Avanzado"
        },
        {
            "course": "Desarrollo de Aplicaciones Móviles",
            "start": "Febrero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "luis.vazquez@example.com",
            "image": "https://cms.rootstack.com/sites/default/files/inline-images/Captura%20de%20pantalla%202024-01-11%20a%20la%28s%29%2014.33.17.jpg",
            "stars": 4.7,
            "category": "Ingeniería",
            "description": "Aprende a desarrollar aplicaciones móviles con Android y iOS.",
            "level": "Intermedio"
        },
        {
            "course": "Desarrollo de Backend",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "mariogarcia@gmail.com",
            "image": "https://www.azulschool.net/wp-content/uploads/2020/05/Databasse-Administrator-1024x709.jpg",
            "stars": 4.4,
            "category": "Ingeniería",
            "description": "Domina el desarrollo de APIs, bases de datos y servidores.",
            "level": "Avanzado"
        },
        {
            "course": "Redes y Ciberseguridad",
            "start": "Enero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "maria.fernandez@example.com",
            "image": "https://www.redseguridad.com/wp-content/uploads/sites/2/2022/01/consejos-ciberseguridad-contra-las-amenazas-de-la-red.jpg",
            "stars": 4.8,
            "category": "Ingeniería",
            "description": "Protege redes y sistemas contra ciberataques.",
            "level": "Intermedio"
        },
        {
            "course": "Inteligencia Artificial y Machine Learning",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "carlos.ramirez@example.com",
            "image": "https://www.uxbi.mx/wp-content/uploads/2023/02/300123_UXB_Postlink_Machine_Learning.jpg",
            "stars": 4.9,
            "category": "Ingeniería",
            "description": "Aprende sobre modelos de IA y redes neuronales.",
            "level": "Avanzado"
        },
        {
            "course": "Robótica y Automatización",
            "start": "Febrero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "fernando.ruiz@example.com",
            "image": "https://advance.unab.cl/assets/uploads/2023/04/400-X-243-Cuales-son-las-diferencias-entre-Automatizacion-y-Robotica.jpg",
            "stars": 4.8,
            "category": "Ingeniería",
            "description": "Diseña e implementa sistemas automatizados y robots.",
            "level": "Intermedio"
        },
        {
            "course": "Desarrollo de Videojuegos con Unity",
            "start": "Enero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "alancarlos032104.com",
            "image": "https://citlafalda.gob.ar/wp-content/uploads/2020/11/videojuegos-unity-3d-ATCONMASFUTURO17-18.png",
            "stars": 4.7,
            "category": "Ingeniería",
            "description": "Crea videojuegos con Unity y C#.",
            "level": "Intermedio"
        },
        {
            "course": "Blockchain y Criptomonedas",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "alancarlos032104@gmail.com",
            "image": "https://strategicplatform.com/hs-fs/hubfs/blockchain%20big%20data.jpg?width=1428&name=blockchain%20big%20data.jpg",
            "stars": 4.6,
            "category": "Ingeniería",
            "description": "Explora la tecnología detrás de las criptomonedas y contratos inteligentes.",
            "level": "Avanzado"
        },

        # Ciencias
        {
            "course": "Astronomía y Astrofísica",
            "start": "Enero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "luislopez@gmail.com",
            "image": "https://noticiasgreenpress.com/wp-content/uploads/2023/09/shutterstock_307424684.jpg",
            "stars": 4.6,
            "category": "Ciencias",
            "description": "Explora el universo y los misterios del espacio.",
            "level": "Intermedio"},
        {
            "course": "Biología Molecular",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "maria@example.com",
            "image": "https://www.ucentral.edu.co/sites/default/files/inline-images/biologia-molecular-ucentral.jpeg",
            "stars": 4.7,
            "category": "Ciencias",
            "description": "Estudia la vida a nivel molecular y sus procesos.",
            "level": "Avanzado"},
        {
            "course": "Química Orgánica",
            "start": "Febrero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "pedro.morales@example.com",
            "image": "https://st1.uvnimg.com/dims4/default/724039b/2147483647/thumbnail/480x270/quality/75/?url=https%3A%2F%2Fuvn-brightspot.s3.amazonaws.com%2Fassets%2Fvixes%2Fbtg%2Fcuriosidades.batanga.com%2Ffiles%2FQue-es-y-para-que-sirve-la-quimica-organica-1.jpg",
            "stars": 4.5, "category": "Ciencias",
            "description": "Descubre la estructura y reactividad de los compuestos del carbono.",
            "level": "Intermedio"},
        {
            "course": "Física Cuántica",
            "start": "Enero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "mariogarcia@gmail.com",
            "image": "https://services.meteored.com/img/article/revolucionario-intentaran-crear-espacio-tiempo-desde-cero-en-un-laboratorio-fisica-cuantica-1698815430058_1024.jpeg",
            "stars": 4.9,
            "category": "Ciencias",
            "description": "Adéntrate en los fundamentos de la mecánica cuántica.",
            "level": "Avanzado"},
        {
            "course": "Ecología y Medio Ambiente",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "diego.martinez@example.com",
            "image": "https://www.ecoportal.net/wp-content/uploads/2023/10/ecologia.jpg",
            "stars": 4.4,
            "category": "Ciencias",
            "description": "Aprende sobre la conservación del medio ambiente y la sostenibilidad.",
            "level": "Básico"},
        {
            "course": "Neurociencia y Comportamiento",
            "start": "Febrero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "beatriz.herrera@example.com",
            "image": "https://anabcn.org/wp-content/uploads/2023/11/neurociencias-1536x691.jpg",
            "stars": 4.7,
            "category": "Ciencias", "description": "Explora cómo el cerebro influye en el comportamiento humano.",
            "level": "Intermedio"},

        {
            "course": "Nutrición y Dietética",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "luislopez@gmail.com",
            "image": "https://aleaconsultadietetica.com/wp-content/uploads/2013/02/alimentacion-1.jpg",
            "stars": 4.6,
            "category": "Salud",
            "description": "Curso enfocado en los principios fundamentales de la nutrición y su aplicación en la salud general.",
            "level": "Intermedio"
        },
        {
            "course": "Primeros Auxilios",
            "start": "Febrero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "roberto.sanchez@example.com",
            "image": "https://yoamoenfermeriablog.com/wp-content/uploads/2019/07/images-17.jpeg",
            "stars": 4.8,
            "category": "Salud",
            "description": "Curso básico para aprender a manejar situaciones de emergencia y aplicar los primeros auxilios adecuados.",
            "level": "Principiante"
        },
        {
            "course": "Psicología Clínica",
            "start": "Enero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "monica.vega@example.com",
            "image": "https://estudiofotografiacreativa.com/wp-content/uploads/2022/09/ramas-psicologia-social-840x473.jpg",
            "stars": 4.9,
            "category": "Salud",
            "description": "Explora las técnicas y teorías fundamentales en la psicología clínica para el tratamiento de trastornos mentales.",
            "level": "Avanzado"
        },
        {
            "course": "Fisioterapia y Rehabilitación",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "daniel.ortega@example.com",
            "image": "https://lostilos.es/wp-content/uploads/2023/08/fISIOTERAPIA.jpg",
            "stars": 4.7,
            "category": "Salud",
            "description": "Este curso ofrece formación sobre técnicas de fisioterapia y rehabilitación para el tratamiento de lesiones físicas.",
            "level": "Intermedio"
        },
        {
            "course": "Medicina Alternativa y Holística",
            "start": "Febrero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "mariana.lopez@example.com",
            "image": "https://lostilos.es/wp-content/uploads/2023/08/fISIOTERAPIA.jpg",
            "stars": 4.6,
            "category": "Salud",
            "description": "Curso introductorio a las prácticas de medicina alternativa y holística para el bienestar integral.",
            "level": "Principiante"
        },

        {
            "course": "Dibujo y Pintura",
            "start": "Enero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "alancarlos032104@gmail.com",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/440px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
            "stars": 4.8,
            "category": "Arte",
            "description": "Curso de introducción a las técnicas básicas de dibujo y pintura, explorando diferentes estilos y medios.",
            "level": "Principiante"
        },
        {
            "course": "Fotografía Digital",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "luislopez@gmail.com",
            "image": "https://www.cooperatingvolunteers.com/wp-content/uploads/2018/02/foto_camara-e1519050718210.jpg",
            "stars": 4.6,
            "category": "Arte",
            "description": "Curso que abarca desde la técnica básica hasta la edición avanzada de fotografías digitales.",
            "level": "Intermedio"
        },
        {
            "course": "Historia del Arte",
            "start": "Febrero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "patricia.torres@example.com",
            "image": "https://blog.facialix.com/wp-content/uploads/2024/05/Historia-del-arte.jpg",
            "stars": 4.7,
            "category": "Arte",
            "description": "Recorrido por las principales corrientes artísticas y su impacto en la cultura visual contemporánea.",
            "level": "Avanzado"
        },
        {
            "course": "Diseño Gráfico",
            "start": "Enero",
            "end": "Junio",
            "year": 2025,
            "teacherEmail": "andrea.fuentes@example.com",
            "image": "https://mediactiu.com/wp-content/uploads/2021/04/Por-que-necesito-contratar-los-servicios-de-diseño-grafico.jpg",
            "stars": 4.9,
            "category": "Arte",
            "description": "Aprende a crear gráficos visuales, desde el diseño de logotipos hasta la creación de campañas publicitarias.",
            "level": "Avanzado"
        },
        {
            "course": "Animación 2D y 3D",
            "start": "Julio",
            "end": "Diciembre",
            "year": 2025,
            "teacherEmail": "mariogarcia@gmail.com",
            "image": "https://www.animatoonstudio.es/wp-content/uploads/2023/04/produccion-video-animacion-2d-3d.png",
            "stars": 4.8,
            "category": "Arte",
            "description": "Explora el mundo de la animación digital, aprendiendo a crear animaciones tanto en 2D como en 3D.",
            "level": "Intermedio"
        }
    ]

    courses_collection = mongo.db.courses

    courses_collection.insert_many(Courses)

    return jsonify(Courses)


@user_bp.route('/update_info', methods=["POST"])
def update_info():
    pass
