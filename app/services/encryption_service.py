import base64

def base_64_decode(input_data):
    try:      
        # Decode base64 data
        output_data = base64.b64decode(input_data)       
        #
        return output_data
    except Exception as e:
        print("base64 decode error " , e)