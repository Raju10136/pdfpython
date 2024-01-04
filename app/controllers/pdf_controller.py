# app/controllers/main_controller.py
from flask import Blueprint, request,jsonify,Response
from app.utils.response_utils import success_response, error_response
from app.services.data_service import get_data,get_data_new,update_data
from app.exceptions.custom_exceptions import CustomException
from app.services.filestorage_service import store_file_base64_array,retrieve_pdf_content
from app.services.pdftools_service import merge_pdfs,gs_compress,overlay_pdf_with_start_page,generate_watermark_pdf,add_watermark,convert_html_pdf
from app.services.encryption_service import base_64_decode
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
        pdf_content = retrieve_pdf_content(output_file)
        encoded_output = base64.b64encode(pdf_content).decode("utf-8")       
        return success_response(encoded_output)
    except CustomException as e:
        print("error ", e)
        return error_response(str(e), e.status_code)

@pdf_blueprint.route("/compress_pdf", methods=["POST"])
def compress_pdf():
    try:
        payload = request.json.get('compress_data')
        #print("input payrload data = ",merge_payload)
        input_dir = DATA + "/compress"
        out_array = store_file_base64_array(payload,input_dir)
        output_file = input_dir + "/output.pdf"
        gs_compress(out_array[0],output_file)
        pdf_content = retrieve_pdf_content(output_file)
        encoded_output = base64.b64encode(pdf_content).decode("utf-8")       
        return success_response(encoded_output)
    except CustomException as e:
        print("error ", e)
        return error_response(str(e), e.status_code)
    
   
@pdf_blueprint.route("/watermark_pdf", methods=["POST"])
def watermark_pdf():
    try:
        input_payload = request.json.get('pdf_data')
        water_mark_text =  request.json.get('water_mark_text')
        #print("input payrload data = ",input_payload)
        # save the file to system
        print(" input received ")
        input_dir = DATA + "/watermark"
        files_array = store_file_base64_array(input_payload,input_dir) 
        print("need to water mark the pdf ")
        water_mark_pdf =  input_dir + "/watermark.pdf"
        generate_watermark_pdf(water_mark_text,water_mark_pdf)
        print("water mark done")
        # after water mark is generated then genrate overlay
        output_file = input_dir + "/output.pdf"
        add_watermark(files_array[0],output_file,water_mark_pdf)
        print("adding water mark ")
        pdf_content = retrieve_pdf_content(output_file)
        encoded_output = base64.b64encode(pdf_content).decode("utf-8")       
        return success_response(encoded_output)
    except CustomException as e:
        print("error ", e)
        return error_response(str(e), e.status_code)
    
    
@pdf_blueprint.route("/overlay_pdf", methods=["POST"])
def overlay_pdf():
    try:
        payload = request.json.get('overlay_data')
        #print("input payrload data = ",merge_payload)
        input_dir = DATA + "/overlay"
        out_array = store_file_base64_array(payload,input_dir)
        merge_array = out_array[1:]
        overlay_file = input_dir + "/overlay.pdf"
        #merge pdf
        merge_pdfs(merge_array,overlay_file)
        # output file
        output_file = input_dir + "/output.pdf"
        # start page number
        start_page_number = int(request.json.get('start_page',10))
        #execute the overlay logic now
        overlay_pdf_with_start_page(out_array[0],overlay_file,output_file,start_page_number)
        # retrive the contet of the pdf file
        pdf_content = retrieve_pdf_content(output_file)
        # encode the content
        encoded_output = base64.b64encode(pdf_content).decode("utf-8")  
        # success response     
        return success_response(encoded_output)
    except CustomException as e:
        print("error ", e)
        return error_response(str(e), e.status_code)


@pdf_blueprint.route("/get_pdf", methods=["POST"])
def get_pdf():
    # Get the Base64-encoded location from the GET parameter
    encoded_location = request.json.get('location', '')
    try:
        # Decode the Base64-encoded location
        decoded_location = base64.b64decode(encoded_location).decode('utf-8')
        print("decoed _location " , decoded_location)
        # Retrieve the PDF content using the function
        pdf_content = retrieve_pdf_content(decoded_location)
        # Set the content type to 'application/pdf' for the response
        encoded_output = base64.b64encode(pdf_content).decode("utf-8")
        #response = Response(pdf_content, content_type='application/pdf')
        # Optionally, set a filename for the downloaded PDF
        #response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
        #return response
        return success_response(encoded_output)
    except Exception as e:
        # Handle any errors
        print("error",str(e))
        return error_response(str(e), e.status_code)
    
@pdf_blueprint.route("/html_to_pdf", methods=["POST"])
def html_to_pdf():
    try:
        input_payload = request.json.get('html_data')
        html_content = base_64_decode(input_payload[0])
        print("html decoded " , html_content)
        #print("input payrload data = ",merge_payload)
        input_dir = DATA + "/htmltopdf"      
        output_file = input_dir + "/output.pdf"
        convert_html_pdf(html_content,output_file)
        print("conversion over")
        pdf_content = retrieve_pdf_content(output_file)
        encoded_output = base64.b64encode(pdf_content).decode("utf-8")       
        return success_response(encoded_output)
    except CustomException as e:
        print("error ", e)
        return error_response(str(e), e.status_code)
