from functools import wraps
from flask import request, g, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from .app import *

EXPIRED = 31536000


def generate_token(user, expiration=EXPIRED):
	s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
	token = s.dumps({
		'ID': str(user.get('id')),
		'email': user.get('email'),
		'role': user.get('role'),
		'username': user.get('username'),
		'userlogin': user.get('userlogin')
	}).decode('utf-8')
	return token


def verify_token(token):
	s = Serializer(app.config['SECRET_KEY'])
	try:
		data = s.loads(token)
	except (BadSignature, SignatureExpired):
		return None
	return data


def requires_auth(*roles):
	"""Проверка авторизации с ролями"""
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			token = request.headers.get('Authorization', None)
			# print("TOKEN",token)
			if token:
				string_token = token.encode('ascii', 'ignore')
				user = verify_token(string_token)
				if user:
					g.current_user = user
					# print(vars(g))
					if roles:
						if g.current_user['role'] not in roles:
							return jsonify(message="Authentication is required to access this resource"), 401
					return f(*args, **kwargs)
			return jsonify(message="Authentication is required to access this resource"), 401
		return wrapped
	return wrapper
