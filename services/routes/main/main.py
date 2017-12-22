import datetime
import random
import string

from flask import g
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
		data = PGHelper.selectAll("select * from (SELECT DISTINCT ON (e1.name, e2.name, p_name) e1.name as e1_name, e2.name as e2_name, divergent.time as time, divergent.diff as diff, CONCAT(p.base_key, '-', p.quote_key) as p_name FROM divergent LEFT JOIN exchanges AS e1 ON (exchanges1_id=e1.id) LEFT JOIN exchanges AS e2 ON (exchanges2_id=e2.id) LEFT JOIN pairs as p ON (pair_id=p.id) WHERE divergent.time > '" + time + "' ORDER BY e1.name, e2.name, p_name, divergent.time desc) as q order by diff desc LIMIT 200")
	else:
		where_str = "divergent.time > '" + time + "'"
		if filters.get('filters').get('exchanges'):
			where_str = where_str + "AND e1.id IN(" + ",".join(filters.get('filters').get('exchanges')) + ") OR e2.id IN(" + ",".join(filters.get('filters').get('exchanges')) + ")"
		if filters.get('filters').get('pairs'):
			where_str = where_str + "AND p.id IN(" + ",".join(filters.get('filters').get('pairs')) + ")"
		if filters.get('filters').get('actives'):
			pass
		data = PGHelper.selectAll("select * from (SELECT DISTINCT ON (e1.name, e2.name, p.pair_name) e1.name as e1_name, e2.name as e2_name, divergent.time as time, divergent.diff as diff, p.pair_name as p_name FROM divergent LEFT JOIN exchanges AS e1 ON (exchanges1_id=e1.id) LEFT JOIN exchanges AS e2 ON (exchanges2_id=e2.id) LEFT JOIN pairs as p ON (pair_id=p.id) WHERE " + where_str + " ORDER BY e1.name, e2.name, p.pair_name, divergent.time desc) as q order by diff desc LIMIT 200")

	return jsonify(valid=True, result=data)


@app.route("/user/main", methods=["POST"])
@requires_auth()
def getMain():
	user = PGHelper.selectOne("SELECT username, userlogin FROM users WHERE id=" + g.current_user.get('ID'))
	if user:
		user["cash"] = 0.00000007
		user["hold"] = 0.00000007
		return jsonify(valid=True, result=user)
	else:
		return jsonify(valid=False, error="no_user")


@app.route("/user/settings", methods=["POST"])
@requires_auth()
def getSettings():
	filters = request.get_json()
	filters = ObjectHelper.cleanEmptyValues(filters)

	if filters.get('user'):
		if filters.get('data'):
			PGHelper.execute_vars("UPDATE users SET settings=%s WHERE id=%s", (filters.get('data'), filters.get('user')))
			return jsonify(valid=True)
		else:
			data = PGHelper.selectOne("SELECT settings, id FROM users WHERE id=" + filters.get('user'))
			return jsonify(valid=True, result=data)
	else:
		return jsonify(valid=False, error="no_user")
