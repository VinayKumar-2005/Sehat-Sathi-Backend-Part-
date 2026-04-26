from flask import jsonify

def success_response(message, data=None, status_code=200):
    response = {
        'success': True,
        'message': message
    }
    # ✅ Merge data into the root dictionary
    # This allows 'token' to be at the top level for your test script
    if data:
        response.update(data)
        
    return jsonify(response), status_code

def error_response(message, status_code=400):
    return jsonify({
        'success': False,
        'error': message
    }), status_code