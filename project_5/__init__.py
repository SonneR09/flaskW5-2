from flask import Flask

from project_5.config import Config
from project_5.models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Имортируем представление
from project_5.views import *

if __name__ == "__main__":
    app.run()
