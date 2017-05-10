import os
from flask import Flask,render_template, url_for, redirect, flash
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import services.nlpservice.nlp_service as nlp
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOADED_FILES_DEST = 'temp/'
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx'])

app.config['MONGO_DBNAME'] = 'textdocuments'
app.config['MONGO_URI']= 'mongodb://192.168.99.100:32768/textDocumentdb'
app.config['UPLOADED_FILES_DEST'] = UPLOADED_FILES_DEST


mongo = PyMongo(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#repository
def add_text_document_to_db(name, text):
    documents = mongo.db.documents
    document_id = documents.insert({'name': name, 'text': text})
    new_document = documents.find_one({'_id': document_id})
    output = {'name' : new_document['name'], 'text' : new_document['text']}
    return jsonify({'result' : output})

@app.route('/')
def showMachineList():
    return render_template('list.html')

@app.route('/documents', methods=['GET'])
def get_all_textDocuments():
  documents = mongo.db.documents
  output = []
  for d in documents.find():
    output.append({'name' : d['name'], 'text' : d['text']})
  return jsonify({'result' : output})

@app.route('/documents/<string:name>', methods=['GET'])
def get_one_document(name):
  documents = mongo.db.documents
  d = documents.find_one({'name' : name})
  if d:
      output = {'name': d['name'], 'text': d['text']}
  else:
      output = "no document found with name " + name
  return jsonify({'result' : output})

@app.route('/document', methods=['POST'])
def add_document():
  name = request.json['name']
  text = request.json['text']
  return add_text_document_to_db(name, text)

@app.route('/file', methods=['POST', 'GET'])
def add_file():
 #   check whether the request has a file
   if 'file' not in request.files:
      os.flash('No file part')
      return 'No file sent'
   file = request.files['file']
   if file and allowed_file(file.filename):
       path = os.path.join(app.config['UPLOADED_FILES_DEST'], secure_filename(file.filename))
       file.save(path);
       text = nlp.text_file_to_string(path)
       name = file.filename
       add_text_document_to_db(name, text)   
       return 'file uploaded successfully'
   else:
       return 'File type not supported (yet)', 500
   
   
@app.route('/documents/<string:name>', methods=['DELETE'])
def delete_document(name):
    mongo.db.documents.delete_many({"name": name});
    return "Document deleted succesfully"

@app.route('/summarize', methods=['GET'])
def summarize_documents():
  total_text= ""
  documents = mongo.db.documents
  for document in documents.find():
      total_text += "\n" + document['text']
  return nlp.summarize_text(total_text)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')