import pytest
from app import create_app, db
from app.models import Clinic, CompartmentSize, Transfer, Supply, Route, TransferType
from datetime import datetime, date, time
import uuid

@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost/test_drombo'})
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

# ---------------------- POST /transfers ----------------------
def test_post_transfer(client):
    clinic = Clinic(id="clinic1", name="Test Clinic", latitude=0.0, longitude=0.0)
    db.session.add(clinic)
    db.session.commit()

    transfer_data = {
        "type": "pedido",
        "request_date": "2025-05-01",
        "requester": "Dr. Smith",
        "start_date": "2025-05-02",
        "end_date": "2025-05-03",
        "start_time": "10:00:00",
        "end_time": "12:00:00",
        "compartment": "mediano",
        "urgency": "media",
        "status": "pendiente",
        "clinic_id": "clinic1",
        "supplies": [
            {"name": "Guantes", "quantity": 100, "weight": 1}
        ]
    }

    response = client.post("/transfers", json=transfer_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["type"] == "pedido"
    assert data["clinic_id"] == "clinic1"
    assert len(data["supplies"]) == 1

# ---------------------- GET /transfers ----------------------
def test_get_transfers(client):
    response = client.get("/transfers")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# ---------------------- GET /transfers/<id> ----------------------
def test_get_transfer_by_id(client):
    # Insert a Transfer first
    transfer = Transfer(
        id="transfer1",
        type=TransferType.REQUEST,  # Use the Enum member here
        request_date=date.today(),
        start_date=date.today(),
        end_date=date.today(),
        start_time=time(10, 0),
        end_time=time(12, 0),
        compartment=CompartmentSize.MEDIUM,  # Correct enum value for compartment size
        clinic_id="clinic1"
    )
    clinic = Clinic(id="clinic1", name="Test Clinic", latitude=0.0, longitude=0.0)
    db.session.add(clinic)
    db.session.add(transfer)
    db.session.commit()

    response = client.get("/transfers/transfer1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == "transfer1"

# ---------------------- DELETE /transfers/<id> ----------------------
def test_delete_transfer(client):
    transfer = Transfer(
        id="transfer2",
        type=TransferType.REQUEST,  # Use the Enum member here
        request_date=date.today(),
        start_date=date.today(),
        end_date=date.today(),
        start_time=time(10, 0),
        end_time=time(12, 0),
        compartment=CompartmentSize.MEDIUM,
        clinic_id="clinic1"
    )
    clinic = Clinic(id="clinic1", name="Test Clinic", latitude=0.0, longitude=0.0)
    db.session.add(clinic)
    db.session.add(transfer)
    db.session.commit()

    response = client.delete("/transfers/transfer2")
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()["message"]

# ---------------------- GET /routes ----------------------
def test_get_routes_all_and_filtered(client):
    # Insert route
    route = Route(id="route1", date=date(2025, 5, 1), time=time(9, 0))
    db.session.add(route)
    db.session.commit()

    # Without date param
    res_all = client.get("/routes")
    assert res_all.status_code == 200
    assert len(res_all.get_json()) >= 1

    # With valid date
    res_filtered = client.get("/routes?date=01-05-2025")
    assert res_filtered.status_code == 200
    assert any(r["id"] == "route1" for r in res_filtered.get_json())

    # With invalid date
    res_bad = client.get("/routes?date=invalid-date")
    assert res_bad.status_code == 400
