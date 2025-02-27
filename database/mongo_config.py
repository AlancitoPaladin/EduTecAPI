from flask_pymongo import PyMongo

mongo = PyMongo()  # Instancia global de PyMongo


def init_db(app):
    # Configura la URI de MongoDB en la aplicación Flask
    app.config["MONGO_URI"] = "mongodb://localhost:27017/EduTecDatabase"
    mongo.init_app(app)  # Inicializa PyMongo con la app
