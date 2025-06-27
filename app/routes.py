from flask import Blueprint, abort, jsonify, request
from app.models import Clinic, Route, RouteStatus, Transfer
from app import db
import uuid
from datetime import date, datetime, time
from app.models import Transfer, Supply, TransferType, CompartmentSize, UrgencyLevel, TransferStatus


transfers_bp = Blueprint('transfers', __name__)
main = Blueprint('main', __name__)

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

    try:
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            print(date)
            routes = Route.query.filter(Route.date == date, Route.status == RouteStatus.READY_FOR_START).all()
        else:
            routes = Route.query.all()
    
    except ValueError:
        return jsonify({"error": "Date format must be DD-MM-YYYY"}), 400

    return jsonify([route.to_dict() for route in routes]), 200

# get_routes - return all routes 

# get_clinics - return all clinics
@transfers_bp.route('/clinics', methods=['GET'])
def get_clinics():
    clinics = Clinic.query.all()
    return jsonify([clinic.to_dict() for clinic in clinics]), 200


# postpone_route - TBD

# send_route_to_rigitech (BLOQUEADO POR FRANCO)


## CRONJOBS

# recalculate_routes - Every 5 minutes
# update_transfer_status - Once per day
# create_routin_transfers - Once per week 



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