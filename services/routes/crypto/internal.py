from flask import request, jsonify

from helpers.objectHelper import ObjectHelper
from helpers.pgHelper import PGHelper
from services.app import app
from services.auth import requires_auth


@app.route("/user/internal/list", methods=["POST"])
@requires_auth()
def getInternalList():
	data = PGHelper.selectAll("SELECT percent, internal.time, e1.name as exchange, a1.name as asset1, a2.name as asset2, a3.name as asset3 FROM internal LEFT JOIN exchanges AS e1 ON (exchange=e1.id) LEFT JOIN assets AS a1 ON (asset0=a1.id) LEFT JOIN assets AS a2 ON (asset1=a2.id) LEFT JOIN assets AS a3 ON (asset2=a3.id) ORDER BY percent desc")
	return jsonify(valid=True, result=data)


@app.route("/user/internal/assets", methods=["POST"])
@requires_auth()
def getInternalAssets():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)

	print(filters)
	if filters.get('id') and filters.get('data') and len(filters.get('data')) > 1:
		summ = 0
		for k, v in enumerate(filters.get('data')):
			if filters.get('data')[k+1]:
				pair = v + "_" + filters.get('data')[k+1]
			else:
				pair = v + "_" + filters.get('data')[0]

			stage1 = PGHelper.selectOne("SELECT pair, ask FROM tickers_source WHERE pair='" + pair + "' AND exchange='" + filters.get('id') + "' ORDER BY time DESC LIMIT 1")

			if stage1:
				if summ == 0:
					summ = stage1.get('ask')
				else:
					summ = summ / stage1.get('ask')
			else:
				summ = 0

		return jsonify(valid=True, result=summ)
	else:
		return jsonify(valid=False, error="no_data")
