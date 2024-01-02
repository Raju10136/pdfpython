# app/controllers/main_controller.py
from flask import Blueprint, request,jsonify,Response
from app.utils.response_utils import success_response, error_response
from app.services.data_service import get_data,get_data_new,update_data
from app.exceptions.custom_exceptions import CustomException
from app.services.filestorage_service import store_file_base64_array,retrieve_pdf_content
from app.services.pdftools_service import merge_pdfs
import base64

pdf_blueprint = Blueprint("pdf", __name__)
DATA="D:/data/pdfdata"

@pdf_blueprint.route("/merge_pdf", methods=["POST"])
def merge_pdf():
    try:
        merge_payload = request.json.get('merge_data')
        #print("input payrload data = ",merge_payload)
        input_dir = DATA + "/merge"
        merged_array = store_file_base64_array(merge_payload,input_dir)
        output_file = input_dir + "/output.pdf"
        merge_pdfs(merged_array,output_file)
        encoded_output = base64.b64encode(output_file.encode("utf-8")).decode("utf-8")
        print("merged array ", encoded_output)
        #data = {"output":encoded_output}
        return success_response(encoded_output)
    except CustomException as e:
        print("error ", e)
        return error_response(str(e), e.status_code)

@pdf_blueprint.route("/get_pdf", methods=["GET"])
def get_pdf():
    # Get the Base64-encoded location from the GET parameter
    encoded_location = request.args.get('location', '')
    try:
        # Decode the Base64-encoded location
        decoded_location = base64.b64decode(encoded_location).decode('utf-8')
        # Retrieve the PDF content using the function
        pdf_content = retrieve_pdf_content(decoded_location)
        # Set the content type to 'application/pdf' for the response
        response = Response(pdf_content, content_type='application/pdf')
        # Optionally, set a filename for the downloaded PDF
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response
    except Exception as e:
        # Handle any errors
        return error_response(str(e), e.status_code)
