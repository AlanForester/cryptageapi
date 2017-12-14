import logging
import waitress

from services.app import app


def main():
	waitress.serve(app, port=5000, _quiet=True)

	# Создаем свой логгер
	logger = logging.getLogger('waitress2')
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(formatter)
	logger.addHandler(ch)


if __name__ == '__main__':
	main()
