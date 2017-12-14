import json
from datetime import datetime
from flask import request, jsonify
from helpers.objectHelper import ObjectHelper
from helpers.pgHelper import PGHelper
from ...services.auth import generate_token
from ...helpers.auth import Users

from ...services.app import app


@app.route("/api/auth/register", methods=["POST"])
def register():
	incoming = request.get_json()
	if incoming.get('data'):
		try:
			incoming = json.loads(incoming.decode())
			incoming = ObjectHelper.cleanEmptyValues(incoming)
			if incoming.get('userlogin') and incoming.get('password'):
				user = PGHelper.selectOne("SELECT password FROM users WHERE userlogin='" + incoming.get('userlogin') + "'")
				if user:
					return jsonify(valid=False, error="exist")
				else:
					password = Users.generate_new_password(incoming.get('password'))
					role = PGHelper.selectOne("SELECT get_role_id('admin')")
					id = PGHelper.execute_vars("INSERT INTO users (userlogin, password, email, banned, username, role, created) VALUES (%s, %s, %s, false, %s, %s, %s) RETURNING id", (incoming.get('userlogin'), password, incoming.get('email') if incoming.get('email') else "", incoming.get('username') if incoming.get('username') else "", role, datetime.utcnow()))

					user = {"id": id, "email": incoming.get('email'), "role": role, "username": incoming.get('username') if incoming.get('username') else "", "userlogin": incoming.get('userlogin')}
					token = generate_token(user)

					return jsonify(valid=True, token=token)
			else:
				return jsonify(valid=False, error="no_data")
		except BaseException:
			return jsonify(valid=False, error="server_error")
	else:
		return jsonify(valid=False, error="no_input")
