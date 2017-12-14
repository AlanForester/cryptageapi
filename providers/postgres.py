import psycopg2
import providers.globals as gvars

from providers.config import get_config
from psycopg2.extras import RealDictCursor


def get_postgres():
	if not gvars.APP_POSTGRES:
		gvars.APP_POSTGRES = Database()
	return gvars.APP_POSTGRES


class Database:
	connections_count = 5
	connection_used = 0

	username = None
	password = None
	hostname = None
	port = None
	database = None

	_connections = []

	def __init__(self):
		config = get_config()
		self.username = config.get_postgres_username()
		self.password = config.get_postgres_password()
		self.hostname = config.get_postgres_hostname()
		self.port = config.get_postgres_port()
		self.database = config.get_postgres_database()

		i = 0
		while i < self.connections_count:
			self._connections.append(self.connect())
			i += 1

	def connect(self):
		con = psycopg2.connect(
			database=self.database,
			user=self.username,
			host=self.hostname,
			port=self.port,
			password=self.password,
			cursor_factory=RealDictCursor
		)
		con.autocommit = True
		return con

	def get_cursor(self):
		cursor = None
		try:
			cursor = self._connections[self.connection_used].cursor()
			if self.connection_used >= len(self._connections) - 1:
				self.connection_used = 0
		except psycopg2.InterfaceError:
			i = 0
			self._connections = []
			while i < self.connections_count:
				self._connections.append(self.connect())
				i += 1
			cursor = self._connections[self.connection_used].cursor()
			if self.connection_used >= len(self._connections) - 1:
				self.connection_used = 0
		except psycopg2.DatabaseError:
			print("PG недоступно. Пытаюсь переподключиться")
			i = 0
			self._connections = []
			while i < self.connections_count:
				self._connections.append(self.connect())
				i += 1
			cursor = self._connections[self.connection_used].cursor()
			if self.connection_used >= len(self._connections) - 1:
				self.connection_used = 0

		finally:
			return cursor
