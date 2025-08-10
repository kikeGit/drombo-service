import logging
import threading
from flask import Blueprint, abort, jsonify, request
from app.models import Clinic, Operation, OperationStatus, RigiRoute, Route, RouteStatus, Transfer
from app.db import db
import uuid
import time as time_god
from datetime import date, datetime, time, timedelta, timezone
from app.models import Transfer, Supply, TransferType, CompartmentSize, UrgencyLevel, TransferStatus
from app.rigi import RestClient


transfers_bp = Blueprint('transfers', __name__)
main = Blueprint('main', __name__)


rigi_client = RestClient()


@main.route('/') 
def index():
    return jsonify({"message": "Hola desde Flask!"})


# get_transfers
@transfers_bp.route('/transfers', methods=['GET'])
def get_transfers():
    transfers = Transfer.query.order_by(Transfer.request_date.desc()).all()
    return jsonify([transfer.to_dict() for transfer in transfers])

# get_transfer (get one)
@transfers_bp.route('/transfers/<string:transfer_id>', methods=['GET'])
def get_transfer(transfer_id):
    transfer = Transfer.query.get(transfer_id)
    if transfer is None:
        abort(404, description="Transfer not found")
    return jsonify(transfer.to_dict())


# post_transfer
@transfers_bp.route('/transfers', methods=['POST'])
def post_transfer():
    data = request.get_json()

    try:
        validate_transfer_data(data)

        transfer = Transfer(
            id=data.get("id", str(uuid.uuid4())),
            type=TransferType(data["type"]),
            request_date=datetime.fromisoformat(data["request_date"]).date(),
            requester=data.get("requester"),
            start_date=datetime.fromisoformat(data["start_date"]).date(),
            end_date=datetime.fromisoformat(data["end_date"]).date(),
            start_time=time.fromisoformat(data["start_time"]),
            end_time=time.fromisoformat(data["end_time"]),
            compartment=CompartmentSize(data["compartment"]),
            urgency=UrgencyLevel(data.get("urgency", "baja")),
            status=TransferStatus(data.get("status", "pendiente")),
            clinic_id=data["clinic_id"],
            routine_id=data.get("routine_id"),
            route_id=data.get("route_id"),
            operation_id=data.get("operation_id")
        )

        # Create associated supplies if any
        supplies_data = data.get("supplies", [])
        for supply_data in supplies_data:
            supply = Supply(
                id=str(uuid.uuid4()),
                name=supply_data["name"],
                quantity=supply_data["quantity"],
                weight=supply_data["weight"],
                notes=supply_data.get("notes"),
                transfer=transfer  # automatically sets transfer_id
            )
            db.session.add(supply)

        db.session.add(transfer)
        db.session.commit()

        return jsonify(transfer.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



# update_transfer

# delete_transfer
@transfers_bp.route('/transfers/<string:transfer_id>', methods=['DELETE'])
def delete_transfer(transfer_id):
    transfer = Transfer.query.get(transfer_id)

    if not transfer:
        return jsonify({"error": "Transfer not found"}), 404

    try:
        db.session.delete(transfer)
        db.session.commit()
        return jsonify({"message": f"Transfer {transfer_id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# get_routes (date) - return all routes scheduled for today
@transfers_bp.route('/routes', methods=['GET'])
def get_routes():
    date_str = request.args.get("date")
    status_str = request.args.get("status")

    filters = []

    # Handle date filter
    if date_str:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            filters.append(Route.date == date)
        except ValueError:
            return jsonify({"error": "Date format must be YYYY-MM-DD"}), 400

    # Handle status filter
    if status_str:
        # Validate status
        try:
            status_enum = RouteStatus[status_str]
            filters.append(Route.status == status_enum)
        except KeyError:
            return jsonify({
                "error": f"Invalid status '{status_str}'. Valid statuses are: {[s.name for s in RouteStatus]}"
            }), 400

    # Build query with optional filters
    #ordenar
    routes = (Route.query
        .filter(*filters)
        .order_by(Route.date.asc(), Route.start_time.asc())
        .all()
    )

    return jsonify([route.to_dict() for route in routes]), 200

@transfers_bp.route('/start-route', methods=['POST'])
def start_route():
    #rigi_client.get_routes()
    data = request.get_json()

    if not data or 'route_id' not in data:
        return jsonify({"error": "Missing 'route_id' in request body"}), 400

    route_id = data['route_id']
    route: Route = Route.query.get(route_id)
    logging.info(f'route_id: {route_id}')


    if not route:
        return jsonify({"error": f"Route with id {route_id} not found"}), 404

    # Parse ordered transfer IDs
    ordered_ids = route.routed_transfers_order.split(",")

    # Load transfers in order
    ordered_transfers = []
    for transfer_id in ordered_ids:
        transfer: Transfer = next((t for t in route.transfers if t.id == transfer_id), None) # for pirado
        if transfer:
            ordered_transfers.append(transfer)


    current_clinic: Clinic = None
    last_transfer = None
    
    dron_id = 42 # dron 152, simulator 105, 42
    battery_id = 'CIE-ER-02-042'
    pilot_id = 3000086
    mari_id = 3000080

    while ordered_transfers:
        transfer = ordered_transfers.pop(0)

        transfers_batch = [transfer]
        
        while ordered_transfers:    
            if ordered_transfers[0].clinic_id == transfer.clinic_id:
                transfers_batch.append(ordered_transfers.pop(0)) # t1, t2,
            else:
                break
         
        origin_id = '0' # hospital central
        if current_clinic:
            origin_id = current_clinic.id


        destination_id = transfer.clinic_id
        rigi_route: RigiRoute = (
            RigiRoute.query
            .filter(
                RigiRoute.clinic_origin == origin_id,
                RigiRoute.clinic_destination == destination_id
            )
            .first()
        )

        if last_transfer:
            s_time = number_to_time(time_to_number(last_transfer.estimated_arrival_time) + current_clinic.average_wait_time)
            # 1. Convert s_time ("HH:MM") to datetime.time
            hours, minutes = map(int, s_time.split(":"))
            s_time_obj = time(hour=hours, minute=minutes)

            # 2. Combine date and time
            naive_dt = datetime.combine(route.date, s_time_obj)
            # If it's actually in local time (e.g., UTC−3), use:
            # from datetime import timedelta
            local_dt = naive_dt.replace(tzinfo=timezone(timedelta(hours=-3)))
            utc_dt = local_dt.astimezone(timezone.utc)
            # 4. Format final schedule_time
            schedule_time = utc_dt.strftime("%Y-%m-%d %H:%M")
        else:
            # Parse string into naive datetime
            naive_dt = datetime.strptime(route.scheduled_date_time, "%Y-%m-%d %H:%M")

            # Localize to UTC−3
            local_dt = naive_dt.replace(tzinfo=timezone(timedelta(hours=-3)))

            # Convert to UTC
            utc_dt = local_dt.astimezone(timezone.utc)

            # Format the final UTC string
            schedule_time = utc_dt.strftime("%Y-%m-%d %H:%M")
        
        last_transfer = transfers_batch[-1]
        current_clinic = transfer.clinic
        operation_name = f"DROMBO - Vuelo a {current_clinic.name}"

        schedule_time = '2025-07-27 18:44'
        op_payload = {
            "project": 51,
            "name": operation_name,
            "scheduledTime": schedule_time,
            "route": rigi_route.rigi_id,
            "payload": route.weight_at_depot / 1000,
            #"drone": dron_id,
            "batteries": [battery_id],
            "pic": pilot_id,
            "groundOperators": [mari_id],
            "comments": "Test"
        }

        logging.info(f"operation payload: {op_payload}")

        rigi_operation_id = rigi_client.create_operation(op_payload)
        if not rigi_operation_id:
            return jsonify({"error": "Error al crear operación de retorno al depósito"}), 502
        
        time_god.sleep(1)
        logging.info(f"rigi_operation_id: {rigi_operation_id}")

        if not rigi_operation_id:
            return jsonify({"error": f"Error de comunicación con RigiTech"}), 502

        operation = Operation(
            id=str(uuid.uuid4()),
            route=route, # la ruta local
            status=OperationStatus.CREATED,
            estimated_time=rigi_route.flight_time_minutes,
            rigi_operation_id=rigi_operation_id,
            rigi_route_id=rigi_route.rigi_id,
            origin_clinic_id=origin_id,
            destination_clinic_id=destination_id,
            scheduled_time = schedule_time
        )

        operation.transfers = transfers_batch.copy()
        db.session.add(operation)

    route.status = RouteStatus.READY_FOR_START # lo actualiza ?

    depot_route: RigiRoute = (
        RigiRoute.query
        .filter(
            RigiRoute.clinic_origin == destination_id, # trampita, el valor de destination_id se puede usar como origin en la proxima operacion
            RigiRoute.clinic_destination == '0'
        )
        .first()
    )

    if last_transfer:
        s_time = number_to_time(time_to_number(last_transfer.estimated_arrival_time) + current_clinic.average_wait_time)
        # 1. Convert s_time ("HH:MM") to datetime.time
        hours, minutes = map(int, s_time.split(":"))
        s_time_obj = time(hour=hours, minute=minutes)

        # 2. Combine date and time
        naive_dt = datetime.combine(route.date, s_time_obj)
        # If it's actually in local time (e.g., UTC−3), use:
        # from datetime import timedelta
        local_dt = naive_dt.replace(tzinfo=timezone(timedelta(hours=-3)))
        utc_dt = local_dt.astimezone(timezone.utc)
        # 4. Format final schedule_time
        schedule_time = utc_dt.strftime("%Y-%m-%d %H:%M")
    else:
        # Parse string into naive datetime
        naive_dt = datetime.strptime(route.scheduled_date_time, "%Y-%m-%d %H:%M")

        # Localize to UTC−3
        local_dt = naive_dt.replace(tzinfo=timezone(timedelta(hours=-3)))

        # Convert to UTC
        utc_dt = local_dt.astimezone(timezone.utc)

        # Format the final UTC string
        schedule_time = utc_dt.strftime("%Y-%m-%d %H:%M")

    name = f"DROMBO - Vuelta al Hospital Central"
    schedule_time = '2025-07-27 18:44'
    depot_op_payload = {
        "project": 51,
        "name": name,
        "scheduledTime": schedule_time,
        "route": depot_route.rigi_id,
        "payload": route.weight_at_depot / 1000,
        #"drone": dron_id,
        "batteries": [battery_id],
        "pic": pilot_id,
        "groundOperators": [mari_id],
        "comments": "Depot"
    }

    logging.info(f"depot operation payload: {depot_op_payload}")    
    rigi_operation_id = rigi_client.create_operation(depot_op_payload)
    if not rigi_operation_id:
        return jsonify({"error": "Error al crear operación de retorno al depósito"}), 502

    logging.info(f"depot rigi_operation_id: {rigi_operation_id}")

    return_to_depot_operation = Operation(
        id=str(uuid.uuid4()),
        route=route, # la ruta local
        status=OperationStatus.CREATED,
        estimated_time=depot_route.flight_time_minutes,
        rigi_operation_id=rigi_operation_id,
        
        rigi_route_id=depot_route.rigi_id,

        origin_clinic_id=destination_id, # trampita, el valor de destination_id se puede usar como origin en la proxima operacion
        destination_clinic_id='0',
        scheduled_time = schedule_time
    )
    
    for transfer in route.transfers:
        transfer.status = TransferStatus.CONFIRMED

    db.session.add(return_to_depot_operation)
    db.session.commit()

    return jsonify(route.to_dict()), 200


# get_clinics - return all clinics
@transfers_bp.route('/clinics', methods=['GET'])
def get_clinics():
    clinics = Clinic.query.all()
    return jsonify([clinic.to_dict() for clinic in clinics]), 200


REQUIRED_TRANSFER_FIELDS = [
    "type", "request_date", "start_date", "end_date",
    "start_time", "end_time", "compartment", "clinic_id"
]

REQUIRED_SUPPLY_FIELDS = [
    "name", "quantity", "weight"
]

def validate_transfer_data(data):
    # Check required Transfer fields
    missing_fields = [field for field in REQUIRED_TRANSFER_FIELDS if data.get(field) is None]
    if missing_fields:
        abort(400, description=f"Missing required transfer fields: {', '.join(missing_fields)}")

    # If there are supplies, validate them too
    supplies = data.get("supplies", [])
    for i, supply in enumerate(supplies):
        missing_supply_fields = [field for field in REQUIRED_SUPPLY_FIELDS if supply.get(field) is None]
        if missing_supply_fields:
            abort(400, description=f"Supply {i + 1} is missing required fields: {', '.join(missing_supply_fields)}")

def time_to_number(time_to_ask):
    hora_str = time_to_ask
    if isinstance(time_to_ask, time):
        hora_str = time_to_ask.strftime("%H:%M")
    
    hours, minutes = map(int, hora_str.split(":"))
    return hours + minutes / 60

def number_to_time(num):
    hours = int(num)
    minutes = round((num - hours) * 60)
    return f"{hours:02d}:{minutes:02d}"