# app/controllers/main_controller.py
from flask import Blueprint, request
from app.utils.response_utils import success_response, error_response
from app.services.data_service import get_data, update_data
from app.exceptions.custom_exceptions import CustomException

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/api/main/get_data", methods=["GET"])
def get_data_route():
    try:
        data = get_data()
        return success_response(data)
    except CustomException as e:
        return error_response(str(e), e.status_code)

@main_blueprint.route("/api/update_data", methods=["PUT"])
def update_data_route():
    try:
        # Assuming JSON payload with an "update" field
        update_payload = request.get_json()
        updated_data = update_data(update_payload["update"])
        return success_response(updated_data, "Data updated successfully")
    except CustomException as e:
        return error_response(str(e), e.status_code)