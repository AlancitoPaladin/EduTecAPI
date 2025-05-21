import os
from flask import Flask
from api.factory import create_app
from database.mongo_config import init_db, mongo  # Importa esto de mongo_config.py

app = create_app()

# Configuración adicional si lo necesitas
app.config["DEBUG"] = True

# Inicializa la conexión con MongoDB Atlas
init_db(app)

if __name__ == "__main__":
    app.run()