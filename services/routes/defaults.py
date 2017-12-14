from flask import Blueprint, render_template
from ..app import app
defaults_api = Blueprint('defaults_api', __name__)


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html'), 410


@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
	return path + " not found", 404

