from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import enum
import atexit

from app import create_app
from app.db import db  # ✅ MUST come from app.db, not redefined
from app.cronjobs import Cronjob
from app.rigi import RestClient, WebSocket
from app.make_routing import build_flight_time_matrix

app = create_app()

def main():
    with app.app_context():
        db.create_all()
        print("✅ Tables created.")
        
        # Start your cronjob system with access to app context
        scheduler = Cronjob(db, app)
        scheduler.plan_routes()
        print(build_flight_time_matrix())
        #scheduler.start()
        #client = RestClient()
        #websocket = WebSocket()
        #client.get_simulator_list()
        #client.start_simulator()
        #client.get_routes()
        #client.create_operation()
        #client.get_operation_by_id(18580)
        #client.delete_operation(18580)


if __name__ == '__main__':
    main()
    app.run(debug=False)