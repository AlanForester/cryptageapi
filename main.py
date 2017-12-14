import logging
import waitress

from providers.providers import Providers
from services.bootstrap import app


class App(object):
	def __init__(self):
		service = Providers.config().launch_service
		if service == "api":
			print("Started on 8089")
			waitress.serve(app, port=8089, _quiet=True)
			#
			# Создаем свой логгер
			logger = logging.getLogger('waitress2')
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			ch = logging.StreamHandler()
			ch.setLevel(logging.DEBUG)
			ch.setFormatter(formatter)
			logger.addHandler(ch)

	@staticmethod
	def start():
		App()


def main():
	App.start()


if __name__ == '__main__':
	main()
