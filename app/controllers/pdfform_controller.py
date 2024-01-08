# app/controllers/main_controller.py
from flask import Blueprint, request,jsonify,Response
from app.utils.response_utils import success_response, error_response
from app.services.data_service import get_data,get_data_new,update_data
from app.exceptions.custom_exceptions import CustomException
from app.services.filestorage_service import store_file_base64_array,retrieve_pdf_content
from app.services.pdfform_service import read_pdf_form_fields,fill_form_fields
from app.services.encryption_service import base_64_decode


pdfform_blueprint = Blueprint("pdfform", __name__)
DATA="E:/test/data/pdfdata"

@pdfform_blueprint.route("/get_fields", methods=["POST"])
def get_fields():
    try:
        payload = request.json.get('pdf_data')
        #print("input payrload data = ",merge_payload)
        input_dir = DATA + "/pdfform"
        out_array = store_file_base64_array(payload,input_dir)
        #output_file = input_dir + "/output.pdf"
        #pdf_location = input_dir + "/temptestfill.pdf" 
        print("enterering in read")
        fields = read_pdf_form_fields(out_array[0])
        #merged_array = store_file_base64_array(merge_payload,input_dir)
        #output_file = input_dir + "/output.pdf"
        ##merge_pdfs(merged_array,output_file)
        #@pdf_content = retrieve_pdf_content(output_file)
        #encoded_output = base64.b64encode(pdf_content).decode("utf-8")
        data = {"test":"test"}       
        return success_response(fields)
    except CustomException as e:
        print("error ", e)
        return error_response(str(e), e.status_code)
    
@pdfform_blueprint.route("/fill_fields", methods=["GET"])
def fill_fields():
    try:
        #merge_payload = request.json.get('merge_data')
        #print("input payrload data = ",merge_payload)
        input_dir = DATA + "/pdfform"
        src_location = input_dir + "/temp.pdf" 
        dest_location = input_dir + "/tempfill.pdf"
        print("enterering in read")
        page_fields = [
            [{"name":"Client","value":"raju"},{"name":"Account No","value":"12345"},
                        {"name":"Activation Date","value":"abcdefghigh"}],
                        [],
                        [{"name":"Checklist_AOF","value":'/1'}]
            ]
        fill_form_fields(src_location,page_fields,dest_location)
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

