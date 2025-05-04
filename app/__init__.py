from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_override=None):
    app = Flask(__name__)
    
    # Use custom config if provided (e.g., for testing)
    if config_override:
        app.config.update(config_override)
    else:
        app.config.from_object(Config)

    db.init_app(app)

    from .routes import main, transfers_bp
    app.register_blueprint(main)
    app.register_blueprint(transfers_bp)

    return app