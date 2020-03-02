from app import db, app
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class FileData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))


class FileSchema(ma.Schema):
    class Meta:
        fields = ['number', 'file_id']


file_schema = FileSchema()
files_schema = FileSchema(many=True)
