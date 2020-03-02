from flask import render_template, request, jsonify
from app import app, db
from app.models import File, FileData, file_schema, files_schema
import re

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        query = File(name=file.filename)
        if not re.search(r"\.txt", file.filename):
            return "error: wrong file format"
        if File.query.filter_by(name=file.filename).first():
            return 'error: file already exists'
        else:
            file.save(file.filename)
            with open('./' + file.filename) as text:
                lines = [line.rstrip() for line in text]
            file.remove()
            for line in lines:
                print(line)
                reg = re.search(r"\A\+[0-9]{11}\z", line)
                if not reg:
                    return "error: wrong number " + line
            db.session.add(query)
            db.session.commit()
            for line in lines:
                filename = File.query.filter_by(name=file.filename).first()
                query = FileData(number=line, file_id=filename.id)
                db.session.add(query)
            db.session.commit()
            return 'file uploaded successfully'


@app.route('/load', methods=['GET'])
def get_json():
    if request.method == 'GET':
        all_files = File.query.all()
        all_filedata = FileData.query.all()
        result = files_schema.dump(all_filedata)
        return jsonify(result)
