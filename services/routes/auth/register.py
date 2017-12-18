import json
from datetime import datetime
from flask import request, jsonify
from helpers.objectHelper import ObjectHelper
from helpers.pgHelper import PGHelper
from services.auth import generate_token
from helpers.auth import Users

from services.app import app


@app.route("/site/register", methods=["POST"])
def register():
	incoming = request.get_json()
	incoming = ObjectHelper.cleanEmptyValues(incoming)
	if incoming.get('data'):
		try:
			incoming = incoming.get('data')
			if incoming.get('userlogin') and incoming.get('password') and incoming.get('email'):
				user = PGHelper.selectOne("SELECT password FROM users WHERE userlogin='" + incoming.get('userlogin') + "'")
				if user:
					return jsonify(valid=False, error="exist")
				else:
					password = Users.generate_new_password(incoming.get('password'))
					role = PGHelper.selectOne("SELECT get_role_id('admin')")
					PGHelper.execute_vars("INSERT INTO users (userlogin, password, email, banned, username, role, created) VALUES (%s, %s, %s, false, %s, %s, %s)", (incoming.get('userlogin'), password, incoming.get('email') if incoming.get('email') else "", incoming.get('username') if incoming.get('username') else "", role.get('get_role_id'), datetime.utcnow()))
					ids = PGHelper.selectOne("SELECT id FROM users WHERE userlogin='"+incoming.get('userlogin')+"' AND email='"+incoming.get('email')+"'")
					if ids and ids.get('id'):
						user = {"id": ids.get('id'), "email": incoming.get('email'), "role": role, "username": incoming.get('username') if incoming.get('username') else "", "userlogin": incoming.get('userlogin')}
						token = generate_token(user)
						return jsonify(valid=True, token=token)
					else:
						return jsonify(valid=False, error="server_error")
			else:
				return jsonify(valid=False, error="no_data")
		except BaseException:
			return jsonify(valid=False, error="exception")

	else:
		return jsonify(valid=False, error="no_input")


@app.route("/site/emailex", methods=["POST"])
def emailex():
	incoming = request.get_json()
	incoming = ObjectHelper.cleanEmptyValues(incoming)
	if incoming.get('email'):
		user = PGHelper.selectOne("SELECT userlogin FROM users WHERE email='" + incoming.get('email') + "'")
		if user:
			return jsonify(valid=True, result=True)
		else:
			return jsonify(valid=True, result=False)
	else:
		return jsonify(valid=False, error="no_data")


@app.route("/site/loginex", methods=["POST"])
def loginex():
	incoming = request.get_json()
	incoming = ObjectHelper.cleanEmptyValues(incoming)
	if incoming.get('userlogin'):
		user = PGHelper.selectOne("SELECT userlogin FROM users WHERE userlogin='" + incoming.get('userlogin') + "'")
		if user:
			return jsonify(valid=True, result=True)
		else:
			return jsonify(valid=True, result=False)
	else:
		return jsonify(valid=False, error="no_data")
