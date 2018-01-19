from flask import g
from flask import request, jsonify

from helpers.objectHelper import ObjectHelper
from helpers.pgHelper import PGHelper
from services.app import app
from services.auth import requires_auth


@app.route("/user/robots/list", methods=["POST"])
@requires_auth()
def getRobotsList():
	# filters = request.get_json()
	# filters = ObjectHelper.cleanEmptyValues(filters)

	data = PGHelper.selectAll("SELECT robots.summ as summ, robots.safe as safe, signals.id as sig_id, signals.name as signame, signals.type, e1.name as e1_name, e2.name as e2_name, a1.name as a1_name, a2.name as a2_name, a3.name as a3_name, signals.data2, u.userlogin, u.username FROM robots LEFT JOIN signals ON(robots.signal=signals.id) LEFT JOIN exchanges AS e1 ON (exchange1=e1.key) LEFT JOIN exchanges AS e2 ON (exchange2=e2.key) LEFT JOIN assets AS a1 ON (asset1=a1.symbol) LEFT JOIN assets AS a2 ON (asset2=a2.symbol) LEFT JOIN assets AS a3 ON (asset3=a3.symbol) LEFT JOIN users AS u ON (user_id=u.id)")
	return jsonify(valid=True, result=data)


@app.route("/user/robots/set", methods=["POST"])
@requires_auth()
def getRobotsSet():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)
	if filters.get('summ') and filters.get('safe') and filters.get('signal'):
		if filters.get('id'):
			PGHelper.execute_vars("UPDATE robots SET signal = %s, summ = %s, safe = %s WHERE id = %s", (int(filters.get('signal')), float(filters.get('summ')), filters.get('safe'), int(filters.get('id'))))
		else:
			PGHelper.execute_vars("INSERT INTO robots (signal, summ, safe) VALUES(%s, %s, %s)", (int(filters.get('signal')), float(filters.get('summ')), filters.get('safe')))
		return jsonify(valid=True)
	else:
		return jsonify(valid=False, error="no_data")


@app.route("/user/robots/del", methods=["POST"])
@requires_auth()
def getRobotsDel():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)
	if filters.get('id'):
		PGHelper.execute_vars("DELETE FROM robots WHERE id = %s", (int(filters.get('id'))))
	return jsonify(valid=True)
