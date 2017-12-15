from flask import jsonify
from helpers.pgHelper import PGHelper
from services.app import app
from services.auth import requires_auth


@app.route("/user/markets", methods=["POST"])
@requires_auth()
def getMarkets():
	data = PGHelper.selectAll("SELECT id, title FROM exchanges ORDER BY id DESC")
	return jsonify(valid=True, result=data)
