from flask import jsonify

def api_response(success, message, data=None, status_code=200):
    """
    Standardized API Response format for SehatSaathi.
    """
    response = {
        "success": success,
        "message": message,
        "data": data or {}
    }
    return jsonify(response), status_code