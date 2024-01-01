from app.exceptions.custom_exceptions import CustomException
from app.utils.response_utils import success_response, error_response
import base64
import os
# In-memory data store (replace this with a database in a real-world scenario)
#data_store = {"example_key": "example_value"}
#data_store_new = {"example_ttt_raj": "example_zzz_junnu"}
def create_directory_from_file_path(file_path):
    # Extract the directory path from the full file path
    directory_path = os.path.dirname(file_path)

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def store_file(binary_data,file_location):
    # create a direcoty if not existed
    create_directory_from_file_path(file_location)
    # create a file 
    # Save binary data to a PDF file
    with open(file_location, 'wb') as f:
        f.write(binary_data)


def store_file_from_base64(base64_data,file_location):
    try:      
        # Decode base64 data
        binary_data = base64.b64decode(base64_data)
        # store fie
        store_file(binary_data,file_location)
        #
        return True
    except CustomException as e:
        return error_response(str(e), e.status_code)
# store multiple files
def store_file_base64_array(input_array,input_directory):
    try:
        #loop the files
        for index, base64_data in enumerate(input_array, start=1):
            file_name = f"file_{index}.pdf"
            file_location = input_directory + "/" +  file_name
            store_file_from_base64(base64_data,file_location)
        return True
    except CustomException as e:
        return error_response(str(e), e.status_code) 