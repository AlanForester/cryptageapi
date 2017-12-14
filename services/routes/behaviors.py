from datetime import datetime
from ..app import app
from providers.config import get_config
from flask import request


@app.after_request
def after_request(response):
	import logging

	logger = logging.getLogger('waitress2')
	strr = datetime.utcnow().strftime("%d-%m %H:%M:%S") + " - " + str(response.status_code) + " - " + (request.headers.get('X-Real-IP') if request.headers.get('X-Real-IP') else request.remote_addr) + " - " + request.method + " - " + request.path
	logger.warning(strr)

	if get_config().prod is False:
		response.headers.add('Access-Control-Allow-Origin', '*')
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
		response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response
