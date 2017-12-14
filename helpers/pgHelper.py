from providers.providers import Providers



class PGHelper:
	@staticmethod
	def selectOne(query):
		cur = Providers.postgres().get_cursor()
		cur.execute(query)
		return cur.fetchone()

	@staticmethod
	def selectAll(query):
		cur = Providers.postgres().get_cursor()
		cur.execute(query)
		return cur.fetchall()

	@staticmethod
	def query(query):
		cur = Providers.postgres().get_cursor()
		return cur.execute(query)

	@staticmethod
	def execute_vars(query, var):
		cur = Providers.postgres().get_cursor()
		return cur.execute(query, var)

	@staticmethod
	def insertDB(par1, par2, par3, par4, par5, par6, par7):
		cur = Providers.postgres().get_cursor()
		cur.execute("select update_conversion (%s, %s, %s, %s, %s, %s, %s)", (par1, par2, par3, par4, par5, par6, par7))
