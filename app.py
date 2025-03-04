import os
import configparser
from flask import Flask, request, jsonify
from api.factory import create_app

# Load configuration file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

app = create_app()

# Configuraciones de la app
app.config["DEBUG"] = True
app.config["MONGO_URI"] = config.get("PROD", "DB_URI", fallback="mongodb://localhost:27017/EduTecDatabase")

if __name__ == "__main__":
    app.run()
