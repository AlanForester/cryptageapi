import copy
import datetime
import dateutil.parser as parser
import re


class ObjectHelper:
	@staticmethod
	def cleanEmptyValues(obj:dict or list, soft=False, moresoft=False):
		objj = copy.deepcopy(obj)
		regex = r"<[^>]+>"

		if type(obj) == dict:
			iter = obj.items()
		else:
			iter = enumerate(obj)

		for key, val in iter:
			if (type(val) == dict or type(val) == list) and key != 'history' and not isinstance(val, datetime.date):
				objj[key] = ObjectHelper.cleanEmptyValues(val, soft, moresoft)
				if len(objj[key]) == 0 and key != 'scripts':
					del objj[key]
			else:
				if (val == "" or val is False or val == 0 or val is None) and soft is False:
					if key != 'wm' and val != 'wmstatus' and key != 'splitLandings' and key != 'status':
						del objj[key]
				else:
					if soft is True and val is None:
						del objj[key]
					if key == 'visitedAt' or key == 'createdAt':
						if isinstance(val, datetime.date):
							if val.timestamp() <= 0:
								del objj[key]
						else:
							val = parser.parse(val)
							if val.timestamp() <= 0:
								del objj[key]
							else:
								objj[key] = val
					else:
						if type(val) == str and moresoft is False:
							val = val.replace("'", "\'")
							val = val.replace('"', '\"')
							val = val.replace('<', '&lt;')
							val = val.replace('>', '&gt;')
							matches = re.finditer(regex, val)
							for v in matches:
								# print("ОПАЧИРИК", val, v.group())
								val = val.replace(v.group(), "")
						try:
							if val is not None:
								objj[key] = val
						except IndexError:
							pass
		return objj

	@staticmethod
	def merge(original, update):
		for key, value in original.items():
			if key not in update:
				update[key] = value
			elif isinstance(value, dict):
				ObjectHelper.merge(value, update[key])
		return update
