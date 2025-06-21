from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import enum
import atexit

from app import create_app
from app.db import db  # ✅ MUST come from app.db, not redefined
from app.cronjobs import Cronjob

app = create_app()

def main():
    with app.app_context():
        db.create_all()
        print("✅ Tables created.")
        
        # Start your cronjob system with access to app context
        scheduler = Cronjob(db, app)
        scheduler.start()


if __name__ == '__main__':
    main()
    app.run(debug=False)