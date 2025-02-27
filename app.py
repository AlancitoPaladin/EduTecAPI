import os
import configparser
from flask import Flask, request, jsonify
from api.factory import create_app

# Load configuration file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Create the Flask app
app = create_app()

# Set app configurations
app.config["DEBUG"] = True
app.config["MONGO_URI"] = config.get("PROD", "DB_URI", fallback="mongodb://localhost:27017/default_db")

# Run the app
if __name__ == "__main__":
    app.run()
