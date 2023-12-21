from flask import Flask, jsonify
from pdfapi import overlay_with_start



app = Flask(__name__)

@app.route('/', methods=['GET'])
def greet():
    input_files=["data/overlay/1.pdf","data/overlay/2.pdf","data/overlay/3.pdf","data/overlay/4.pdf","data/overlay/5.pdf"]
    input_pdf_path = "data/template.pdf"
    output_file=overlay_with_start(input_pdf_path,input_files,42)
    return jsonify(message='Hello, World!')

if __name__ == '__main__':
    #input_files=["data/overlay/1.pdf","data/overlay/2.pdf","data/overlay/3.pdf","data/overlay/4.pdf","data/overlay/5.pdf"]
    #input_pdf_path = "data/template.pdf"
    #output_file=overlay_with_start(input_pdf_path,input_files,42)
    app.run(debug=True,port=5001)