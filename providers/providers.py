from providers import config, redis, postgres


class Providers(object):
    @staticmethod
    def postgres():
        return postgres.get_postgres()

    @staticmethod
    def redis():
        return redis.get_redis()

    @staticmethod
    def config():
        return config.get_config()
