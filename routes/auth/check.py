from flask import request, jsonify
from ...services.auth import verify_token
from ...services.app import app


@app.route("/api/auth/check", methods=["POST"])
def is_token_valid():
    token = request.headers.get('Authorization', None)
    if token:
        is_valid = verify_token(token)
        if is_valid:
            return jsonify(token_is_valid=True)
    return jsonify(token_is_valid=False), 403
