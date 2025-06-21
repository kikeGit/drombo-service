from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.cronjobs import Cronjob
from app.db import db
from flask_cors import CORS

#from app.models import Clinic, Transfer, Supply, Route, Operation, Routine

def create_app(config_override=None):
    app = Flask(__name__)
    CORS(app)
    
    # Use custom config if provided (e.g., for testing)
    if config_override:
        app.config.update(config_override)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    #cronjob.start()

    from .routes import main, transfers_bp
    app.register_blueprint(main)
    app.register_blueprint(transfers_bp)

    return app