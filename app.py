from flask import Flask, request, jsonify
import requests
import io
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route("/extract-pdf-text", methods=["POST"])
def extract_text():
    data = request.json
    download_url = data.get("downloadUrl")
    if not download_url:
        return jsonify({"error": "Missing downloadUrl"}), 400

    # Download the PDF
    response = requests.get(download_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to download file"}), 500

    try:
        # Extract text using PyMuPDF
        pdf_bytes = io.BytesIO(response.content)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
