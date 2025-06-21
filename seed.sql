-- Truncate all tables to start fresh
TRUNCATE TABLE operations CASCADE;
TRUNCATE TABLE transfers CASCADE;
TRUNCATE TABLE supplies CASCADE;
TRUNCATE TABLE routes CASCADE;
TRUNCATE TABLE clinics CASCADE;
TRUNCATE TABLE routines CASCADE;

-- Insert Clinics (no dependencies)
INSERT INTO clinics (id, name, latitude, longitude, average_wait_time) VALUES
('1', 'Policlinica Centro', -34.9011, -56.1645, 0.2),
('2', 'Policlinica Norte', -34.8808, -56.1805, 1.2),
('3', 'Policlinica Sur', -34.9210, -56.1510, 1),
('4', 'Policlinica Oeste', -34.9050, -56.1950, 0.7);


INSERT INTO transfers (
    id, type, request_date, requester, start_date, end_date,
    start_time, end_time, compartment, urgency, status,
    clinic_id
) VALUES
('t1', 'ENVIO', '2025-06-16', 'Dr. A', '2025-06-20', '2025-06-20', '10:00:00', '13:00:00', 'SMALL', 'LOW', 'PENDING', '1'),
('t2', 'PEDIDO', '2025-06-16', 'Dr. B', '2025-06-20', '2025-06-21', '11:30:00', '18:30:00', 'MEDIUM', 'MEDIUM', 'PENDING', '2'),
('t3', 'ENVIO', '2025-06-16', 'Dr. C', '2025-06-20', '2025-06-25', '09:00:00', '13:00:00', 'LARGE', 'HIGH', 'PENDING', '3'),
('t4', 'PEDIDO', '2025-06-16', 'Dr. D', '2025-06-20', '2025-06-25', '15:00:00', '17:00:00', 'SMALL', 'LOW', 'PENDING', '4'),
('t5', 'ENVIO', '2025-06-16', 'Dr. E', '2025-06-21', '2025-06-24', '14:00:00', '16:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '2');


INSERT INTO supplies (id, name, weight, quantity, notes, transfer_id) VALUES
('s1', 'Guantes', 1000, 5, 'Caja mediana', 't1'),
('s2', 'Jeringas', 2000, 7, 'Caja grande', 't2'),
('s3', 'Suero', 500, 15, 'Frágil', 't3'),
('s4', 'Alcohol', 750, 4, NULL, 't4'),
('s5', 'Mascarillas', 1300, 6, 'Uso urgente', 't5'),
('s6', 'Vendas', 1200, 3, NULL, 't1'),
('s7', 'Analgesicos', 800, 2, NULL, 't3');