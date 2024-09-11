import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
def create_app() -> Flask:
    app_context = os.getenv('FLASK_CONTEXT')
    
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.resources import home
    app.register_blueprint(home, url_prefix='/api/v1')

    
    
    @app.shell_context_processor
    def shell_context():
        return {"app": app}
    
    return app