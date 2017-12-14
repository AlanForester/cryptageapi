import json
from flask import request, jsonify

from services.auth import generate_token
from helpers.auth import Users
from services.app import app


@app.route("/site/login", methods=["POST"])
def authenticate():
	incoming = request.get_json()
	if incoming:
		if incoming and 'userlogin' in incoming and 'password' in incoming:
			user = Users.get_user_with_user_and_password(incoming.get("userlogin"), incoming.get("password"))
			if user:
				if user.get('deleted'):
					return jsonify(valid=False, error="deleted")
				if user.get('blocked'):
					return jsonify(valid=False, error="banned")
				return jsonify(valid=True, token=generate_token(user))
			else:
				return jsonify(valid=False, error="incorrect"), 200
		return jsonify(valid=False, error="no_info"), 200
	else:
		return jsonify(valid=False, error="no_data"), 200
