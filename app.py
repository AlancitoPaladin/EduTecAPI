import os
import configparser
from api.factory import create_app

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

app = create_app()

app.config["DEBUG"] = True
app.config["MONGO_URI"] = config.get("PROD", "DB_URI", fallback="mongodb://localhost:27017/default_db")

if __name__ == "__main__":
    app.run()
