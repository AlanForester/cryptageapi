from providers.providers import Providers
from models.mongoQuery import MongoQuery
from helpers.queryHelper import QueryHelper


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

	@staticmethod
	def tmpHitPG(hit, sub, valute, isHit):
		cur = Providers.postgres().get_cursor()
		result = []

		subs = {}
		if len(sub) > 0:
			for i, val in enumerate(sub):
				subs[int(val.get('number'))] = val.get('value')

		countryname = None
		regionname = None
		cityname = None
		country = MongoQuery.findOne("countries", {'iso': hit.get('countryISO')})
		if country and country.get('names'):
			countryname = country.get('names').get('ru')

		if hit.get('region'):
			region = MongoQuery.findOne("regions", {'_id': hit.get('region')})
			if region and region.get('names'):
				regionname = region.get('names').get('ru') if region.get('names').get('ru') else region.get('names').get('en')

		if hit.get('city'):
			city = MongoQuery.findOne("cities", {'_id': hit.get('city')})
			if city and city.get('names'):
				cityname = city.get('names').get('ru') if city.get('names').get('ru') else city.get('names').get('en')

		offer = QueryHelper.getOfferById(hit.get('offer'))
		stream = QueryHelper.getStreamById(hit.get('stream'))
		source = QueryHelper.getSourceById(hit.get('source'))

		tback = True if hit.get('trafficBack') else False

		result.append(hit.get('user'))
		result.append(hit.get('offer'))
		result.append(hit.get('stream'))
		result.append(hit.get('landing').get('id') if hit.get('landing') and hit.get('landing').get('id') else None)  # Если вы накасячили и сделали клик без ленда - это упасет вас от проблем
		result.append(hit.get('transit').get('id') if hit.get('transit') and hit.get('transit').get('id') else None)
		result.append(hit.get('purpose'))
		result.append(hit.get('source'))
		result.append(hit.get('country'))
		result.append(hit.get('region'))
		result.append(hit.get('city'))
		result.append(valute)
		result.append(hit.get('device').get('type') if hit.get('device') and hit.get('device').get('type') else None)
		result.append(hit.get('device').get('brand') if hit.get('device') and hit.get('device').get('brand') else None)
		result.append(hit.get('device').get('model') if hit.get('device') and hit.get('device').get('model') else None)
		result.append(hit.get('device').get('isMobile') if hit.get('device') and hit.get('device').get('isMobile') else False)
		result.append(hit.get('device').get('isCrawler') if hit.get('device') and hit.get('device').get('isCrawler') else False)
		result.append(hit.get('device').get('browser').get('type') if hit.get('device') and hit.get('device').get('browser') and hit.get('device').get('browser').get('type') else None)
		result.append(hit.get('device').get('browser').get('name') if hit.get('device') and hit.get('device').get('browser') and hit.get('device').get('browser').get('name') else None)
		result.append(hit.get('device').get('browser').get('version') if hit.get('device') and hit.get('device').get('browser') and hit.get('device').get('browser').get('version') else None)
		result.append(hit.get('device').get('os').get('name') if hit.get('device') and hit.get('device').get('os') and hit.get('device').get('os').get('name') else None)
		result.append(hit.get('device').get('os').get('version') if hit.get('device') and hit.get('device').get('os') and hit.get('device').get('os').get('version') else None)
		result.append(hit.get('device').get('connection').get('type') if hit.get('device') and hit.get('device').get('connection') and hit.get('device').get('connection').get('type') else None)
		result.append(hit.get('device').get('connection').get('isp') if hit.get('device') and hit.get('device').get('connection') and hit.get('device').get('connection').get('isp') else None)
		result.append(hit.get('device').get('connection').get('carrier') if hit.get('device') and hit.get('device').get('connection') and hit.get('device').get('connection').get('carrier') else None)
		result.append(hit.get('device').get('engine').get('name') if hit.get('device') and hit.get('device').get('engine') and hit.get('device').get('engine').get('name') else None)
		result.append(hit.get('device').get('engine').get('version') if hit.get('device') and hit.get('device').get('engine') and hit.get('device').get('engine').get('version') else None)
		result.append(hit.get('device').get('resolution') if hit.get('device') and hit.get('device').get('resolution') else None)
		result.append(hit.get('device').get('language') if hit.get('device') and hit.get('device').get('language') else None)
		result.append(hit.get('utm').get('source') if hit.get('utm') and hit.get('utm').get('source') else None)
		result.append(hit.get('utm').get('medium') if hit.get('utm') and hit.get('utm').get('medium') else None)
		result.append(hit.get('utm').get('content') if hit.get('utm') and hit.get('utm').get('content') else None)
		result.append(isHit)
		result.append(tback)
		result.append(False)
		result.append(0)
		result.append(0)
		result.append(subs.get(1))
		result.append(subs.get(2))
		result.append(subs.get(3))
		result.append(subs.get(4))
		result.append(subs.get(5))
		result.append(subs.get(6))
		result.append(subs.get(7))
		result.append(subs.get(8))
		result.append(subs.get(9))
		result.append(hit.get('createdAt'))
		if hit.get('showcase') and hit.get('showcase').get('visitedAt'):
			result.append(False)
			result.append(False)
			result.append(True)
		elif (not hit.get('landing') or not hit.get('landing').get('visitedAt')) and (not hit.get('showcase') or hit.get('showcase').get('visitedAt')):
			result.append(True)
			result.append(False)
			result.append(False)
		elif (not hit.get('transit') or not hit.get('transit').get('visitedAt')) and (not hit.get('showcase') or hit.get('showcase').get('visitedAt')):
			result.append(False)
			result.append(False)
			result.append(False)
		else:
			result.append(False)
			result.append(True)
			result.append(False)
		result.append(countryname)
		result.append(regionname)
		result.append(cityname)
		result.append(offer.get('title'))
		result.append(stream.get('title'))
		result.append(source.get('title'))
		result.append(hit.get('cost') if hit.get('cost') else 0)

		cur.execute('insert into statistics_clicks("user", offer, stream, landing, transit, purpose, source, country, '
					'region, city, valute, device_type, device_brand, device_model, device_is_mobile, '
					'device_is_crawler, device_browser_type, device_browser_name, device_browser_version, '
					'device_os_name, device_os_version, device_connection_type, device_connection_isp, '
					'device_connection_carrier, device_engine_name, device_engine_version, device_resolution, '
					'device_language, utm_source, utm_medium, utm_content, is_hit, is_tback, is_conversion, '
					'conversion_status, conversion_cost, s1, s2, s3, s4, s5, s6, s7, s8, s9, created_at, is_transit, '
					'is_landing, is_showcase, country_name, region_name, city_name, offer_name, stream_name, '
					'source_name, cpc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
					'%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
					'%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', result)

	@staticmethod
	def tmpConvPG(conv, click, sub, valute, offer, status, cost, reject):
		# изменения от ноды (конверсии)
		# 1.поиск городов/регионов/стран был по клику - теперь по конверсии (может смениться)
		# 2.траффик бек тоже по конверсии
		cur = Providers.postgres().get_cursor()
		result = []

		subs = {}
		if sub and len(sub) > 0:
			for i, val in enumerate(sub):
				subs[int(val.get('number'))] = val.get('value')

		countryname = None
		regionname = None
		cityname = None
		country = MongoQuery.findOne("countries", {'iso': conv.get('countryISO')})
		if country and country.get('names'):
			countryname = country.get('names').get('ru')

		if conv.get('region'):
			region = MongoQuery.findOne("regions", {'_id': conv.get('region')})
			if region and region.get('names'):
				regionname = region.get('names').get('ru') if region.get('names').get('ru') else region.get('names').get('en')

		if conv.get('city'):
			city = MongoQuery.findOne("cities", {'_id': conv.get('city')})
			if city and city.get('names'):
				cityname = city.get('names').get('ru') if city.get('names').get('ru') else city.get('names').get('en')

		stream = QueryHelper.getStreamById(click.get('stream'))
		source = QueryHelper.getSourceById(click.get('source'))

		tback = True if conv.get('trafficBack') else False

		result.append(click.get('user'))
		result.append(click.get('offer'))
		result.append(click.get('stream'))
		result.append(click.get('landing').get('id'))
		result.append(click.get('transit').get('id') if click.get('transit') and click.get('transit').get('id') else None)
		result.append(click.get('purpose'))
		result.append(click.get('source'))
		result.append(conv.get('country') if conv.get('country') else '')
		result.append(conv.get('region') if conv.get('region') else '')
		result.append(conv.get('city') if conv.get('city') else '')
		result.append(valute)
		result.append(conv.get('device').get('type') if conv.get('device') and conv.get('device').get('type') else None)
		result.append(conv.get('device').get('brand') if conv.get('device') and conv.get('device').get('brand') else None)
		result.append(conv.get('device').get('model') if conv.get('device') and conv.get('device').get('model') else None)
		result.append(conv.get('device').get('isMobile') if conv.get('device') and conv.get('device').get('isMobile') else False)
		result.append(conv.get('device').get('isCrawler') if conv.get('device') and conv.get('device').get('isCrawler') else False)
		result.append(conv.get('device').get('browser').get('type') if conv.get('device') and conv.get('device').get('browser') and conv.get('device').get('browser').get('type') else None)
		result.append(conv.get('device').get('browser').get('name') if conv.get('device') and conv.get('device').get('browser') and conv.get('device').get('browser').get('name') else None)
		result.append(conv.get('device').get('browser').get('version') if conv.get('device') and conv.get('device').get('browser') and conv.get('device').get('browser').get('version') else None)
		result.append(conv.get('device').get('os').get('name') if conv.get('device') and conv.get('device').get('os') and conv.get('device').get('os').get('name') else None)
		result.append(conv.get('device').get('os').get('version') if conv.get('device') and conv.get('device').get('os') and conv.get('device').get('os').get('version') else None)
		result.append(conv.get('device').get('connection').get('type') if conv.get('device') and conv.get('device').get('connection') and conv.get('device').get('connection').get('type') else None)
		result.append(conv.get('device').get('connection').get('isp') if conv.get('device') and conv.get('device').get('connection') and conv.get('device').get('connection').get('isp') else None)
		result.append(conv.get('device').get('connection').get('carrier') if conv.get('device') and conv.get('device').get('connection') and conv.get('device').get('connection').get('carrier') else None)
		result.append(conv.get('device').get('engine').get('name') if conv.get('device') and conv.get('device').get('engine') and conv.get('device').get('engine').get('name') else None)
		result.append(conv.get('device').get('engine').get('version') if conv.get('device') and conv.get('device').get('engine') and conv.get('device').get('engine').get('version') else None)
		result.append(conv.get('device').get('resolution') if conv.get('device') and conv.get('device').get('resolution') else None)
		result.append(conv.get('device').get('language') if conv.get('device') and conv.get('device').get('language') else None)
		result.append(click.get('utm').get('source') if click.get('utm') and click.get('utm').get('source') else None)
		result.append(click.get('utm').get('medium') if click.get('utm') and click.get('utm').get('medium') else None)
		result.append(click.get('utm').get('content') if click.get('utm') and click.get('utm').get('content') else None)
		result.append(False)
		result.append(tback)
		result.append(True)
		result.append(status)
		result.append(cost)
		result.append(subs.get(1))
		result.append(subs.get(2))
		result.append(subs.get(3))
		result.append(subs.get(4))
		result.append(subs.get(5))
		result.append(subs.get(6))
		result.append(subs.get(7))
		result.append(subs.get(8))
		result.append(subs.get(9))
		result.append(conv.get('createdAt'))
		result.append(conv.get('order').get('id'))
		result.append(conv.get('goal'))
		result.append(countryname)
		result.append(regionname)
		result.append(cityname)
		result.append(offer.get('title'))
		result.append(stream.get('title'))
		result.append(source.get('title'))
		result.append(reject)

		cur.execute('insert into statistics_clicks("user", offer, stream, landing, transit, purpose, source, country, '
					'region, city, valute, device_type, device_brand, device_model, device_is_mobile, '
					'device_is_crawler, device_browser_type, device_browser_name, device_browser_version, '
					'device_os_name, device_os_version, device_connection_type, device_connection_isp, '
					'device_connection_carrier, device_engine_name, device_engine_version, device_resolution, '
					'device_language, utm_source, utm_medium, utm_content, is_hit, is_tback, is_conversion, '
					'conversion_status, conversion_cost, s1, s2, s3, s4, s5, s6, s7, s8, s9, created_at,order_id, '
					'goal, country_name, region_name, city_name, offer_name, stream_name, source_name, is_duble) '
					'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
					'%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
					'%s, %s, %s, %s, %s, %s, %s, %s, %s)', result)
