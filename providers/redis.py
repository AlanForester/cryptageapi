import redis
import json
import providers.globals as gvars

from providers.config import get_config
from bson import json_util


def get_redis():
	if not gvars.APP_REDIS:
		gvars.APP_REDIS = Redis()
	return gvars.APP_REDIS


class Redis:
	db = None
	hostname = None
	port = None

	_connection = None

	def __init__(self):
		config = get_config()
		self.db = config.get_redis_db()
		self.hostname = config.get_redis_hostname()
		self.port = config.get_redis_port()

		self.connect()

	def connect(self):
		self._connection = redis.StrictRedis(
			host=self.hostname,
			port=self.port,
			db=self.db,
			decode_responses=True  # автоматически декодировать байтовые строки
		)

	def get_connection(self):
		return self._connection

	def delete(self, key):
		return self._connection.delete(key)

	def keys(self, key):
		return self._connection.keys(key)

	def get(self, key):
		result = self._connection.get(key)
		if result:
			return json.loads(result)
		else:
			return None

	def info(self):
		result = self._connection.info()
		return result

	def getUtil(self, key):
		result = self._connection.get(key)
		if result:
			return json.loads(result, object_hook=json_util.object_hook)
		else:
			return None

	def getRaw(self, key):
		result = self._connection.get(key)
		if result:
			return result
		else:
			return None

	def set(self, name, value, ex=None, px=None, nx=False, xx=False):
		return self._connection.set(name, value, ex, px, nx, xx)

	def setex(self, name, time, value):
		return self._connection.setex(name, time, value)

	def exists(self, name):
		return self._connection.exists(name)

	def hset(self, key, field, value, ex=None):
		res = self._connection.hset(key, field, value)
		if ex:
			self._connection.pexpire(key, ex)
		return res

	def hget(self, key, field):
		return self._connection.hget(key, field)

	def hgetall(self, key):
		return self._connection.hgetall(key)

	def hmset(self, key, duct, ex=None):
		# сохраняет объект в хеше (как если бы мы перебирали объект и сохраняли через hset (key objkey val)
		res = self._connection.hmset(key, duct)
		if ex:
			self._connection.pexpire(key, ex)
		return res
