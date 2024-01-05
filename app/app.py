from flask import Flask
from app.utils.response_utils import success_response, error_response

app = Flask(__name__)

# Global response handler
@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    header["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    header["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

# Global error handler
@app.errorhandler(Exception)
def handle_error(error):
    message = "Internal Server Error"
    status_code = 500
    return error_response(message, status_code)

# Import and register routes/controllers
from app.controllers.main_controller import main_blueprint
from app.controllers.pdf_controller import pdf_blueprint
from app.controllers.pdfform_controller import pdfform_blueprint
app.register_blueprint(main_blueprint,url_prefix='/api/main')
app.register_blueprint(pdf_blueprint,url_prefix='/api/pdf')
app.register_blueprint(pdfform_blueprint,url_prefix='/api/pdfform')
