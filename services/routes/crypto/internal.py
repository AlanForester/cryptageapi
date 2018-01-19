from flask import request, jsonify

from helpers.objectHelper import ObjectHelper
from helpers.pgHelper import PGHelper
from services.app import app
from services.auth import requires_auth


@app.route("/user/internal/list", methods=["POST"])
@requires_auth()
def getInternalList():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)
	if filters.get('filters') is None or len(filters.get('filters')) == 0:
		data = PGHelper.selectAll("SELECT internal.id, percent, e1.name as exchange, a1.name as asset1, a2.name as asset2, a3.name as asset3, internal.time as time FROM internal LEFT JOIN exchanges AS e1 ON (exchange=e1.id) LEFT JOIN assets AS a1 ON (asset0=a1.id) LEFT JOIN assets AS a2 ON (asset1=a2.id) LEFT JOIN assets AS a3 ON (asset2=a3.id) ORDER BY percent desc LIMIT 1000")
		for k, v in enumerate(data):
			data[k]['time'] = v.get('time').isoformat()
	else:
		where_str = "WHERE percent > 0 "
		if filters.get('filters').get('exchanges'):
			where_str = where_str + "AND e1.id IN(" + ",".join(filters.get('filters').get('exchanges')) + ")"
		if filters.get('filters').get('assets'):
			where_str = where_str + "AND a1.id IN(" + ",".join(filters.get('filters').get('assets')) + ") OR a2.id IN(" + ",".join(filters.get('filters').get('assets')) + ") OR a3.id IN(" + ",".join(filters.get('filters').get('assets')) + ")"
		if filters.get('filters').get('actives'):
			pass
		where = where_str if where_str else ""
		data = PGHelper.selectAll("SELECT internal.id, percent, e1.name as exchange, a1.name as asset1, a2.name as asset2, a3.name as asset3, internal.time as time FROM internal LEFT JOIN exchanges AS e1 ON (exchange=e1.id) LEFT JOIN assets AS a1 ON (asset0=a1.id) LEFT JOIN assets AS a2 ON (asset1=a2.id) LEFT JOIN assets AS a3 ON (asset2=a3.id) " + where + " ORDER BY percent desc")
		for k, v in enumerate(data):
			data[k]['time'] = v.get('time').isoformat()
	return jsonify(valid=True, result=data)


@app.route("/user/internal/assets", methods=["POST"])
@requires_auth()
def getInternalAssets():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)

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
