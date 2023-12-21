from flask import jsonify

def success_response(data=None, message="Success"):
    response = {
        "status": "success",
        "message": message,
        "data": data,
    }
    return jsonify(response), 200

def error_response(message, status_code):
    response = {
        "status": "error",
        "message": message,
    }
    return jsonify(response), status_code