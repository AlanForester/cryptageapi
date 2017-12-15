from flask import jsonify
from services.app import app
from services.auth import requires_auth


@app.route("/user/actives", methods=["POST"])
@requires_auth()
def getActives():
	data = "{'valid': true, 'data': [{'id': 13, 'name': 'Bitcoin', count: 123},{'id': 1, 'name': 'Зелень', count: 3}]}"
	return jsonify(valid=True, result=data)
