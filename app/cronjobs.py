from datetime import date, time, timedelta
from typing import Tuple
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime
from sqlalchemy import delete

from app import make_routing
from app.models import Route, RouteStatus, Transfer, TransferStatus, UrgencyLevel
from sqlalchemy import and_, func, or_
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update

from app.vrp import Node

import logging
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR



class Cronjob:
    
    distance_matrix = []

    def __init__(self, db, app):
        self.db = db
        self.session = self.db.session
        self.app = app
        self.days = 5

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_listener(self.log_scheduler_events, EVENT_SCHEDULER_STARTED | EVENT_SCHEDULER_SHUTDOWN | EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

         # Configura el logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def shutdown(self):
        self.logger.info("Shutting down scheduler...")
        self.scheduler.shutdown()

    def log_scheduler_events(self, event):
        if event.code == EVENT_SCHEDULER_STARTED:
            self.logger.info("Scheduler has started.")
        elif event.code == EVENT_SCHEDULER_SHUTDOWN:
            self.logger.info("Scheduler has shut down.")
        elif event.code == EVENT_JOB_EXECUTED:
            self.logger.info(f"Job {event.job_id} executed successfully.")
        elif event.code == EVENT_JOB_ERROR:
            self.logger.error(f"Job {event.job_id} raised an error.")


    def start(self):
        self.scheduler.add_job(self.plan_routes, 'interval', minutes=5) # habria q poder configurarlo cada cuanto
        print("Start scheduler")
        self.scheduler.start()
        atexit.register(self.shutdown)

    def plan_routes(self):
        with self.app.app_context():
            self.logger.info("Borrando rutas viejas y preparando traslados")
            self.delete_ready_routes()
            self.logger.info("Calculando nuevas rutas")
            self.recalculate_routes(self.days)
        
    def print_transfer(self, transfer):
        supply_ids = [s.id for s in transfer.supplies] if transfer.supplies else []
        print(f"[{transfer.id}] {transfer.status.name} | {transfer.start_date} → {transfer.end_date} | Clinic: {transfer.clinic_id} | Supplies: {supply_ids}")

    def delete_ready_routes(self):
        # todos los transfers a PENDING
        transfers = Transfer.query.filter(Transfer.status == TransferStatus.CONFIRMED).all()

        for transfer in transfers:
            transfer.status = TransferStatus.PENDING
            transfer.estimated_arrival_date = None
            transfer.estimated_arrival_time = None

        self.db.session.commit()

        routes = Route.query.filter(Route.status == RouteStatus.TENTATIVE).all()
        for route in routes:
            self.db.session.delete(route)

        self.db.session.commit()

    def get_transfers_for_date(self, date: datetime) -> list[Transfer] :
        
        
        transfers = Transfer.query.filter(
            and_(
                func.date(Transfer.start_date) <=  date.date(),  # 20
                func.date(Transfer.end_date) >= date.date(),
                or_(
                    Transfer.status == TransferStatus.PENDING,
                    #Transfer.status == TransferStatus.CONFIRMED
                )
            )
        ).options(
            self.db.joinedload(Transfer.supplies),
            self.db.joinedload(Transfer.clinic)
        ).all()
        
        for t in transfers:
            self.print_transfer(t)
        
        return transfers

    def time_to_number(self, time_to_ask):
        hora_str = time_to_ask
        if isinstance(time_to_ask, time):
            hora_str = time_to_ask.strftime("%H:%M")
        
        hours, minutes = map(int, hora_str.split(":"))
        return hours + minutes / 60

    def number_to_time(self, num):
            hours = int(num)
            minutes = round((num - hours) * 60)
            return f"{hours:02d}:{minutes:02d}"


    def transfer_to_delivery_node(self, transfer: Transfer):
        box_type = str(transfer.compartment.value)
        delivery_name = str(transfer.id)
        delivery_type = str(transfer.type.value).lower()
        service_time = int(transfer.clinic.average_wait_time)
        policlinic = int(transfer.clinic_id)
        time_window = (self.time_to_number(transfer.start_time), self.time_to_number(transfer.end_time))
        demand = transfer.weight

        return Node(box_type=box_type, delivery_name=delivery_name, delivery_type=delivery_type, service_time=service_time, policlinic=policlinic, time_window=time_window, demand=demand )
    

    def cancel_transfers(self, impossible_nodes):
        transfer_ids = [node.delivery_name for node in impossible_nodes]
        
        print("Cancelando nodos imposibles " + str(transfer_ids))

        self.session.execute(
            update(Transfer)
            .where(Transfer.id.in_(transfer_ids))
            .values(status=TransferStatus.REJECTED)
        )
        self.session.commit()

    def update_routed_transfers(self, route_date: date, transfers: list[Transfer], start_times: list[float]):
        
        start_times.pop(0) # los transfers empiezan a partir del segundo

        for index, transfer in enumerate(transfers):
            transfer_time = self.number_to_time(start_times[index])
            
            print("Actualizo el transfer " + str(transfer.id))
            transfer.estimated_arrival_time = transfer_time
            transfer.estimated_arrival_date = route_date
            transfer.status = TransferStatus.CONFIRMED # 

    def create_routes(self, routes, routes_start_service, transfers, date):
        
        for route_index, route in enumerate(routes):
            route_transfers_order = ",".join(node.delivery_name for node in route)
            
            transfers_ids = [node.delivery_name for node in route] # ids de la ruta
            start_times = routes_start_service[route_index]
            
            start_times_order = ",".join(self.number_to_time(start_time) for start_time in start_times)
            
            print(f"Route {route_transfers_order}")
            route_transfers = [transfer for transfer in transfers if transfer.id in transfers_ids]
            self.update_routed_transfers(date, route_transfers, start_times) # se mapean por indice

            start_depot: Node = route[0] # ventana inicio del depot
            end_depot: Node = route[-1] # el ultimo elemento

            route_id = str(uuid.uuid4())
            db_route = Route(
                id=route_id,
                date=date,
                start_time=self.number_to_time(start_depot.get_start_time_window()),
                end_time=self.number_to_time(end_depot.get_start_time_window()),
                routed_transfers_order=route_transfers_order,
                transfers=route_transfers,
                start_times=start_times_order,
                status=RouteStatus.TENTATIVE
            )
            
            self.session.add(db_route)
        self.session.commit()

    # Ejemplo: se ejecuta cada 5 minutos
    def recalculate_routes(self, days=5):
        today = datetime.today()
        
        for i in range(days):
            new_date = today + timedelta(days=i)
            depot = Node(0, 0, (8, 20), 0, 'Depot', None, None) # crear policlinica "depot"

            urgent_deliveries = []
            normal_deliveries = []
            low_deliveries = []
            
            if i == 0:
                current_time_str = datetime.now().strftime("%H:%M")
                print(current_time_str)                
                depot_start_time = self.time_to_number(current_time_str)
                depot.time_window = (depot_start_time, depot.get_end_time_window())
                if depot_start_time > depot.time_window[1]:
                    continue

            print("Recalculando rutas dia " + str(new_date) + "...")

            transfers = self.get_transfers_for_date(new_date)
            for t in transfers:
                delivery_node = self.transfer_to_delivery_node(t)
                
                if t.urgency == UrgencyLevel.HIGH:
                    urgent_deliveries.append(delivery_node)
                if t.urgency == UrgencyLevel.MEDIUM:
                    normal_deliveries.append(delivery_node)
                if t.urgency == UrgencyLevel.LOW:
                    low_deliveries.append(delivery_node)

            routes, routes_start_services, impossible_nodes = make_routing.make_daily_routing(urgent_deliveries, normal_deliveries, low_deliveries, depot)

            self.create_routes(routes, routes_start_services, transfers, new_date)
            self.cancel_transfers(impossible_nodes)
            
            print("Rutas generadas")

