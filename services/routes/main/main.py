import datetime
from flask import request, jsonify

from helpers.objectHelper import ObjectHelper
from helpers.pgHelper import PGHelper
from services.app import app
from services.auth import requires_auth


@app.route("/user/api", methods=["POST"])
@requires_auth()
def getApi():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)

	time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat()
	if filters.get('filters') is None or len(filters.get('filters')) == 0:
		data = PGHelper.selectAll("SELECT e1.name as e1_name, e2.name as e2_name, MIN(divergent.time) as time, AVG(divergent.diff) as diff, p.pair_name as p_name FROM divergent LEFT JOIN exchanges AS e1 ON (exchanges1_id=e1.id) LEFT JOIN exchanges AS e2 ON (exchanges2_id=e2.id) LEFT JOIN pairs as p ON (pair_id=p.id) WHERE divergent.time > '" + time + "' GROUP BY e1.name, e2.name, p.pair_name ORDER BY diff DESC LIMIT 200")
	else:
		where_str = "divergent.time > '" + time + "'"
		if filters.get('filters').get('exchanges'):
			where_str = where_str + "AND e1.id IN(" + ",".join(filters.get('filters').get('exchanges')) + ")"
		if filters.get('filters').get('pairs'):
			where_str = where_str + "AND p.id IN(" + ",".join(filters.get('filters').get('pairs')) + ")"
		if filters.get('filters').get('actives'):
			pass
		data = PGHelper.selectAll("SELECT e1.name as e1_name, e2.name as e2_name, MIN(divergent.time) as time, AVG(divergent.diff) as diff, p.pair_name as p_name FROM divergent LEFT JOIN exchanges AS e1 ON (exchanges1_id=e1.id) LEFT JOIN exchanges AS e2 ON (exchanges2_id=e2.id) LEFT JOIN pairs as p ON (pair_id=p.id) WHERE " + where_str + " GROUP BY e1.name, e2.name, p.pair_name ORDER BY diff DESC LIMIT 200")

	return jsonify(valid=True, result=data)
