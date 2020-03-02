from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filedata.sqlite3'
app.config['UPLOAD_FOLDER'] = '/'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
