from .routes import routes
from .app import app

# REGISTER ROUTES
app.register_blueprint(routes)


