from flask import g
from flask import request, jsonify

from helpers.objectHelper import ObjectHelper
from helpers.pgHelper import PGHelper
from services.app import app
from services.auth import requires_auth


@app.route("/user/signals/list", methods=["POST"])
@requires_auth()
def getSignalsList():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)

	data = PGHelper.selectAll("SELECT signals.id as id, signals.name as signame, signals.type, e1.name as e1_name, e2.name as e2_name, a1.name as a1_name, a2.name as a2_name, a3.name as a3_name, signals.data2, u.userlogin, u.username FROM signals LEFT JOIN exchanges AS e1 ON (exchange1=e1.key) LEFT JOIN exchanges AS e2 ON (exchange2=e2.key) LEFT JOIN assets AS a1 ON (asset1=a1.symbol) LEFT JOIN assets AS a2 ON (asset2=a2.symbol) LEFT JOIN assets AS a3 ON (asset3=a3.symbol) LEFT JOIN users AS u ON (user_id=u.id)")
	return jsonify(valid=True, result=data)


@app.route("/user/signals/set", methods=["POST"])
@requires_auth()
def getSignalsSet():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)
	if filters.get('id') and filters.get('type') and filters.get('percent') and filters.get('name') and filters.get('data1'):
		if filters.get('type') == 1:  # Внутренний
			data = PGHelper.selectOne("SELECT a1.symbol as a1, a2.symbol as a2, a3.symbol as a3, e1.key as e1 FROM internal LEFT JOIN exchanges AS e1 ON (exchange=e1.id) LEFT JOIN assets AS a1 ON (asset0=a1.id) LEFT JOIN assets AS a2 ON (asset1=a2.id) LEFT JOIN assets AS a3 ON (asset2=a3.id) WHERE internal.id=" + str(filters.get('id')))
		else:
			data = PGHelper.selectOne("SELECT p.base_key as a1, p.quote_key as a2, e1.key as e1, e2.key as e2 FROM divergent LEFT JOIN exchanges AS e1 ON (exchanges1_id=e1.id) LEFT JOIN exchanges AS e2 ON (exchanges2_id=e2.id) LEFT JOIN pairs AS p ON (pair_id=p.id) WHERE divergent.id=" + str(filters.get('id')))

		PGHelper.execute_vars("INSERT INTO signals (name, user_id, exchange1, exchange2, asset1, asset2, asset3, type, data1, data2) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (filters.get('name'), int(g.current_user.get("ID")), data.get('e1'), data.get('e2') if data.get('e2') else "", data.get('a1'), data.get('a2'), data.get('a3') if data.get('a3') else "", filters.get('type'), filters.get('data1'), filters.get('percent')))
		return jsonify(valid=True)
	else:
		return jsonify(valid=False, error="no_data")


@app.route("/user/events/list", methods=["POST"])
@requires_auth()
def getEventsList():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)

	data = PGHelper.selectAll("SELECT events.name as signame, events.type, e1.name as e1_name, e2.name as e2_name, a1.name as a1_name, a2.name as a2_name, a3.name as a3_name, events.data2, events.time as time, u.userlogin, u.username FROM events LEFT JOIN exchanges AS e1 ON (exchange1=e1.id) LEFT JOIN exchanges AS e2 ON (exchange2=e2.id) LEFT JOIN assets AS a1 ON (asset1=a1.id) LEFT JOIN assets AS a2 ON (asset2=a2.id) LEFT JOIN assets AS a3 ON (asset3=a3.id) LEFT JOIN users AS u ON (user_id=u.id) ORDER BY events.time DESC")
	return jsonify(valid=True, result=data)
