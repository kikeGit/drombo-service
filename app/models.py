from app.db import db  # ✅ Usa la instancia compartida
import enum
from sqlalchemy.dialects.postgresql import ARRAY

class CompartmentSize(enum.Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "BIG"

class UrgencyLevel(enum.Enum):
    LOW = "baja"
    MEDIUM = "media"
    HIGH = "alta"

class TransferType(enum.Enum):
    PEDIDO = "pedido"
    ENVIO = "envio"

class TransferStatus(enum.Enum):
    PENDING = "pendiente"
    CONFIRMED = "confirmado"
    ON_ROUTE = "en camino"
    REJECTED = "rechazado"
    DELIVERIED = "entregado"

class WeekDay(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

class OperationStatus(enum.Enum):
    CREATED = 'creado'
    IN_PROGRES = 'en camino'
    COMPLETED = 'completado'
    ABORTED = 'abortada'

class Clinic(db.Model):
    __tablename__ = 'clinics'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=False)
    longitude = db.Column(db.Numeric(9, 6), nullable=False)
    average_wait_time = db.Column(db.Integer, nullable=True)

    transfers = db.relationship('Transfer', back_populates='clinic', cascade='all, delete-orphan')

    origin_operations = db.relationship('Operation', foreign_keys='Operation.origin_clinic_id', back_populates='origin_clinic')
    destination_operations = db.relationship('Operation', foreign_keys='Operation.destination_clinic_id', back_populates='destination_clinic')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude)
        }


class Transfer(db.Model):
    __tablename__ = 'transfers'

    id = db.Column(db.String, primary_key=True)
    type = db.Column(db.Enum(TransferType), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    requester = db.Column(db.String, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    compartment = db.Column(db.Enum(CompartmentSize), nullable=False)
    urgency = db.Column(db.Enum(UrgencyLevel), nullable=True, default=UrgencyLevel.LOW)
    status = db.Column(db.Enum(TransferStatus), nullable=True, default=TransferStatus.PENDING)
    estimated_arrival_date = db.Column(db.Date, nullable=True)
    estimated_arrival_time = db.Column(db.Time, nullable=True)

    clinic_id = db.Column(db.String, db.ForeignKey('clinics.id'), nullable=False)
    clinic = db.relationship('Clinic', back_populates='transfers')
    
    supplies = db.relationship('Supply', back_populates='transfer', cascade='all, delete-orphan')

    routine_id = db.Column(db.String, db.ForeignKey('routines.id'), nullable=True)
    routine = db.relationship('Routine', back_populates='transfers')

    route_id = db.Column(db.String, db.ForeignKey('routes.id', ondelete='SET NULL'), nullable=True)
    route = db.relationship('Route', back_populates='transfers')

    operation_id = db.Column(db.String, db.ForeignKey('operations.id'), nullable=True)
    operation = db.relationship('Operation', back_populates='transfers')

    @property
    def weight(self):
        return sum(supply.weight or 0 for supply in self.supplies)
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "request_date": self.request_date.isoformat(),
            "requester": self.requester,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "compartment": self.compartment.value,
            "urgency": self.urgency.value if self.urgency else None,
            "status": self.status.value if self.status else None,
            "clinic_id": self.clinic_id,
            "clinic": self.clinic.to_dict(),
            "routine_id": self.routine_id,
            "route_id": self.route_id,
            "operation_id": self.operation_id,
            "weight": self.weight,
            "supplies": [s.to_dict() for s in self.supplies],
            "estimated_arrival_date": self.estimated_arrival_date.isoformat(),
            "estimated_arrival_time": self.estimated_arrival_time.isoformat(),
        }


class Supply(db.Model):
    __tablename__ = 'supplies'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String, nullable=True)
    
    transfer_id = db.Column(db.String, db.ForeignKey('transfers.id'), nullable=False)
    transfer = db.relationship('Transfer', back_populates='supplies')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "weight": self.weight,
            "notes": self.notes
        }


class RouteStatus(enum.Enum):
    READY_FOR_START = "READY_FOR_START"
    IN_PROCESS = "IN_PROCESS"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    routed_transfers_order = db.Column(db.String, nullable=False) # separado por comas
    start_times = db.Column(db.String, nullable=False) # separado por comas
    status = db.Column(db.Enum(RouteStatus), nullable=False, default=RouteStatus.READY_FOR_START)

    transfers  = db.relationship('Transfer', back_populates='route', cascade='save-update, merge')
    operations = db.relationship('Operation', back_populates='route', cascade='all, delete-orphan')

    @property
    def weight(self):
        return sum(transfer.weight or 0 for transfer in self.transfers)
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "routed_transfers_order": self.routed_transfers_order,
            "transfer_ids": [t.id for t in self.transfers],
            "operation_ids": [op.id for op in self.operations],
            "status": self.status.value,
            "transfers": [transfer.to_dict() for transfer in self.transfers],
            "weight": self.weight
        }


class Operation(db.Model):
    __tablename__ = 'operations'

    id = db.Column(db.String, primary_key=True)
    status = db.Column(db.Enum(OperationStatus), nullable=True, default=OperationStatus.CREATED)
    estimated_time = db.Column(db.Time, nullable=False)
    actual_time = db.Column(db.Time, nullable=True)
    rigitech_id = db.Column(db.String, nullable=False)

    route_id = db.Column(db.String, db.ForeignKey('routes.id'), nullable=False)
    route = db.relationship('Route', back_populates='operations')

    origin_clinic_id = db.Column(db.String, db.ForeignKey('clinics.id'), nullable=False)
    origin_clinic = db.relationship('Clinic', foreign_keys=[origin_clinic_id], back_populates='origin_operations')

    destination_clinic_id = db.Column(db.String, db.ForeignKey('clinics.id'), nullable=False)
    destination_clinic = db.relationship('Clinic', foreign_keys=[destination_clinic_id], back_populates='destination_operations')

    transfers = db.relationship('Transfer', back_populates='operation', cascade='all, delete-orphan')


class Routine(db.Model):
    __tablename__ = 'routines'

    id = db.Column(db.String, primary_key=True)
    type = db.Column(db.Enum(TransferType), nullable=False)
    requester = db.Column(db.String, nullable=False)
    time = db.Column(db.Time, nullable=False)
    compartment = db.Column(db.String, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    urgency = db.Column(db.String, nullable=False)
    frequency = db.Column(ARRAY(db.Enum(WeekDay)), nullable=False)

    transfers = db.relationship('Transfer', back_populates='routine', cascade='all, delete-orphan')

class RigiRoute(db.Model):
    __tablename__ = "rigi_routes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rigi_id = db.Column(db.Integer, nullable=False)

    clinic_origin = db.Column(db.String, db.ForeignKey('clinics.id'), nullable=False)
    clinic_destination = db.Column(db.String, db.ForeignKey('clinics.id'), nullable=False)

    distance_km = db.Column(db.Numeric(10, 2))
    flight_time_minutes = db.Column(db.String, nullable=False)

    # Relationships to Clinic objects
    origin_clinic = db.relationship("Clinic", foreign_keys=[clinic_origin])
    destination_clinic = db.relationship("Clinic", foreign_keys=[clinic_destination])