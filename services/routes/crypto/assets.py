from flask import jsonify
from helpers.pgHelper import PGHelper
from services.app import app
from services.auth import requires_auth


@app.route("/user/assets", methods=["POST"])
@requires_auth()
def getAssets():
	data = PGHelper.selectAll("SELECT id, symbol, name FROM assets ORDER BY id DESC")
	return jsonify(valid=True, result=data)
