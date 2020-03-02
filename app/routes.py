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
        f = request.files['file']
        u = File(name=f.filename)
        if not re.search(r"\.txt", f.filename):
            return "error: wrong file format"
        if File.query.filter_by(name=f.filename).first():
            return 'error: file already exists'
        else:
            f.save("temp.txt")
            with open('./temp.txt') as q:
                lines = [line.rstrip() for line in q]
            print(lines)
            for line in lines:
                print(line)
                r = re.search(r"\A\+[0-9]", line)
                if not r:
                    return "error: wrong number " + line
            db.session.add(u)
            db.session.commit()
            for line in lines:
                q = File.query.filter_by(name=f.filename).first()
                y = FileData(number=line, file_id=q.id)
                db.session.add(y)
            db.session.commit()
            return 'file uploaded successfully'


@app.route('/load', methods=['GET'])
def get_json():
    if request.method == 'GET':
        all_files = File.query.all()
        all_filedata = FileData.query.all()
        result = files_schema.dump(all_filedata)
        return jsonify(result)
