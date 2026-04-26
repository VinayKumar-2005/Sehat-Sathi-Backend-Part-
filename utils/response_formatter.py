def success_response(message, data=None, status_code=200):
    return {
        "status": "success",
        "message": message,
        "data": data
    }, status_code

def error_response(message, status_code=400, errors=None):
    response = {
        "status": "error",
        "message": message
    }
    if errors:
        response["errors"] = errors
    return response, status_code