# app/controllers/main_controller.py
from flask import Blueprint, request,jsonify,Response
from app.utils.response_utils import success_response, error_response
from app.services.data_service import get_data,get_data_new,update_data
from app.exceptions.custom_exceptions import CustomException
from app.services.filestorage_service import store_file_base64_array,retrieve_pdf_content
from app.services.pdftools_service import merge_pdfs,gs_compress,overlay_pdf_with_start_page,generate_watermark_pdf,add_watermark,convert_html_pdf
from app.services.encryption_service import base_64_decode
import base64

pdfform_blueprint = Blueprint("pdfform", __name__)
DATA="D:/data/pdfdata"

@pdfform_blueprint.route("/get_fields", methods=["POST"])
def merge_pdf():
    try:
        #merge_payload = request.json.get('merge_data')
        #print("input payrload data = ",merge_payload)
        input_dir = DATA + "/merge"
        #merged_array = store_file_base64_array(merge_payload,input_dir)
        #output_file = input_dir + "/output.pdf"
        ##merge_pdfs(merged_array,output_file)
        #@pdf_content = retrieve_pdf_content(output_file)
        #encoded_output = base64.b64encode(pdf_content).decode("utf-8")
        data = {"test":"test"}       
        return success_response(data)
    except CustomException as e:
        print("error ", e)
        return error_response(str(e), e.status_code)

