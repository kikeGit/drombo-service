-- Truncate all tables to start fresh
TRUNCATE TABLE operations CASCADE;
TRUNCATE TABLE transfers CASCADE;
TRUNCATE TABLE supplies CASCADE;
TRUNCATE TABLE routes CASCADE;
TRUNCATE TABLE clinics CASCADE;
TRUNCATE TABLE routines CASCADE;

-- Insert Clinics (no dependencies)
INSERT INTO clinics (id, name, latitude, longitude) 
VALUES
    ('clinic1', 'Test Clinic', 40.712776, -74.005974),
    ('clinic2', 'Sample Clinic', 34.052235, -118.243683),
    ('clinic3', 'Clinic 3', 19.434608, -99.135209);  -- Ensure this clinic is inserted before 'operations' data

-- Insert Routes (no dependencies)
INSERT INTO routes (id, date, time)
VALUES
    ('route1', '2025-05-01', '10:00:00'),
    ('route2', '2025-05-02', '11:00:00');

-- Example of Operation INSERT with a valid rigitech_id value
INSERT INTO operations (id, status, estimated_time, actual_time, rigitech_id, route_id, origin_clinic_id, destination_clinic_id)
VALUES 
('operation1', 'CREATED', '08:00:00', NULL, 'rigitech123', 'route1', 'clinic1', 'clinic2'),
('operation2', 'IN_PROGRES', '09:00:00', '10:30:00', 'rigitech124', 'route2', 'clinic2', 'clinic3');


-- Insert Transfers (dependent on clinics, operations, and routes)
INSERT INTO transfers (id, type, request_date, requester, start_date, end_date, start_time, end_time, compartment, urgency, status, clinic_id, routine_id, route_id, operation_id)
VALUES
    ('transfer1', 'pedido', '2025-05-01', 'Requester1', '2025-05-01', '2025-05-01', '10:00:00', '12:00:00', 'MEDIUM', 'LOW', 'PENDING', 'clinic1', NULL, 'route1', 'operation1'),
    ('transfer2', 'envio', '2025-05-02', 'Requester2', '2025-05-02', '2025-05-02', '11:00:00', '13:00:00', 'LARGE', 'HIGH', 'CONFIRMED', 'clinic2', NULL, 'route2', 'operation2');

-- Insert Routines (no direct dependencies, but can reference transfers later)
INSERT INTO routines (id, type, requester, time, compartment, weight, urgency, frequency)
VALUES
    ('routine1', 'pedido', 'Requester1', '08:00:00', 'MEDIUM', 100, 'LOW', ARRAY['MONDAY'::weekday, 'TUESDAY'::weekday, 'WEDNESDAY'::weekday, 'THURSDAY'::weekday]),
    ('routine2', 'envio', 'Requester2', '09:00:00', 'LARGE', 150, 'MEDIUM', ARRAY['MONDAY'::weekday, 'WEDNESDAY'::weekday]);
    
-- Optionally, add Supplies or other related entities as needed.
-- Example:
-- INSERT INTO supplies (id, name, quantity, weight, notes, transfer_id)
-- VALUES ('supply1', 'Medications', 10, 200, 'Urgent', 'transfer1');
