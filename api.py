import os
from flask import Flask, request, jsonify,render_template
from ingest import run_ingestion
from engine import extract_info
from utils import create_index, clear_data

app = Flask(__name__)

data_folder = "data"

@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/ingest/", methods=['POST'])
def ingest_pdf():
    try:
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        file.save(os.path.join(data_folder, file.filename))
        create_index()
        run_ingestion()
        clear_data(data_folder)
        return jsonify({"message": "PDF file ingested successfully"})
    except Exception as e:
        return str(e), 500

@app.route("/extract/", methods=['GET'])
def extract_data():
    try:
        extracted_text = extract_info()
        print(extracted_text)
        return jsonify(extracted_text)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000,debug=True)