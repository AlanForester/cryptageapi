from flask import Flask
from .config import BaseConfig
from providers.providers import Providers
from datetime import datetime
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
Providers.redis().set('api', str(int(datetime.utcnow().timestamp())))

app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object(BaseConfig)

