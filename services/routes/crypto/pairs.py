from flask import jsonify
from helpers.pgHelper import PGHelper
from services.app import app
from services.auth import requires_auth


@app.route("/user/pairs", methods=["POST"])
@requires_auth()
def getPairs():
	data = PGHelper.selectAll("SELECT id, CONCAT(base_name, '-', quote_name) as name FROM pairs WHERE base_key <> '' AND quote_key <> '' ORDER BY id DESC")
	return jsonify(valid=True, result=data)
