# app/controllers/main_controller.py
from flask import Blueprint, request,jsonify
from app.utils.response_utils import success_response, error_response
from app.services.data_service import get_data,get_data_new,update_data
from app.exceptions.custom_exceptions import CustomException
from app.services.filestorage_service import store_file_base64_array

pdf_blueprint = Blueprint("pdf", __name__)
DATA="E:/test/pdata"

@pdf_blueprint.route("/merge_pdf", methods=["POST"])
def merge_pdf():
    try:
        merge_payload = request.json.get('merge_data')
        input_dir = DATA + "/merge"
        store_file_base64_array(merge_payload,input_dir)  
        #print("input payrload data = ",merge_payload)
        data = get_data_new()
        return success_response(data)
    except CustomException as e:
        return error_response(str(e), e.status_code)
