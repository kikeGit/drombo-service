-- Truncate all tables to start fresh
TRUNCATE TABLE operations CASCADE;
TRUNCATE TABLE transfers CASCADE;
TRUNCATE TABLE supplies CASCADE;
TRUNCATE TABLE routes CASCADE;
TRUNCATE TABLE clinics CASCADE;
TRUNCATE TABLE routines CASCADE;

-- Insert Clinics (no dependencies)
INSERT INTO clinics (id, name, latitude, longitude, average_wait_time) VALUES
('0', 'H. de Tacuarembó', -34.9011, -56.1645, 0.2),
('1', 'Tambores', -34.9011, -56.1645, 0.2),
('2', 'Curtina', -34.8808, -56.1805, 1.2),
('3', 'Sauce del Batovi', -34.9210, -56.1510, 1),
('4', 'Ansina', -34.9000, -56.1400, 0.9),
('5', 'Rivera', -34.9100, -56.1700, 1.5),
('6', 'Piedra Sola', -34.9190, -56.1760, 0.2),
('7', 'Paso del Cerro', -31.9190, -55.1760, 0.2);



INSERT INTO transfers (
    id, type, request_date, requester, start_date, end_date,
    start_time, end_time, compartment, urgency, status,
    clinic_id
) VALUES
('t1', 'ENVIO', '2025-07-08', 'Alex Romero', '2025-07-05', '2025-08-08', '10:00:00', '13:00:00', 'SMALL', 'LOW', 'PENDING', '1'),
('t2', 'PEDIDO', '2025-07-08', 'Dr. B', '2025-07-05', '2025-08-08', '11:30:00', '18:30:00', 'MEDIUM', 'MEDIUM', 'PENDING', '2'),
('t3', 'ENVIO', '2025-07-08', 'Dr. C', '2025-07-05', '2025-08-08', '09:00:00', '13:00:00', 'LARGE', 'HIGH', 'PENDING', '3'),
('t4', 'PEDIDO', '2025-07-08', 'Dr. D', '2025-07-05', '2025-08-08', '15:00:00', '17:00:00', 'SMALL', 'LOW', 'PENDING', '4'),
('t5', 'ENVIO', '2025-06-16', 'Dr. E', '2025-07-05', '2025-08-08', '14:00:00', '16:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '2'),
('t6', 'ENVIO', '2025-06-17', 'Dr. F', '2025-07-05', '2025-08-08', '08:00:00', '12:00:00', 'SMALL', 'LOW', 'PENDING', '5'),
('t7', 'PEDIDO', '2025-06-17', 'Dr. G', '2025-07-05', '2025-08-08', '10:30:00', '17:30:00', 'MEDIUM', 'MEDIUM', 'PENDING', '6'),
('t8', 'ENVIO', '2025-06-17', 'Julieta Sosa', '2025-07-03', '2025-08-08', '09:30:00', '15:00:00', 'LARGE', 'HIGH', 'PENDING', '1'),
('t9', 'PEDIDO', '2025-06-18', 'Dr. I', '2025-07-03', '2025-08-08', '14:00:00', '18:00:00', 'SMALL', 'LOW', 'PENDING', '3'),
('t10', 'ENVIO', '2025-06-18', 'Dr. J', '2025-07-05', '2025-08-08', '13:00:00', '16:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '4'),
('t11', 'ENVIO', '2025-06-18', 'Dr. K', '2025-07-05', '2025-08-08', '08:00:00', '11:00:00', 'SMALL', 'LOW', 'PENDING', '2'),
('t12', 'PEDIDO', '2025-06-19', 'Dr. L', '2025-07-05', '2025-08-08', '09:00:00', '12:00:00', 'MEDIUM', 'HIGH', 'PENDING', '3'),
('t13', 'ENVIO', '2025-06-19', 'Dr. M', '2025-07-04', '2025-08-08', '10:00:00', '14:00:00', 'LARGE', 'HIGH', 'PENDING', '4'),
('t14', 'PEDIDO', '2025-06-20', 'Dr. N', '2025-07-03', '2025-08-08', '13:00:00', '16:00:00', 'MEDIUM', 'LOW', 'PENDING', '5'),
('t15', 'ENVIO', '2025-06-20', 'Dr. O', '2025-07-04', '2025-08-08', '14:00:00', '17:00:00', 'SMALL', 'MEDIUM', 'PENDING', '6'),
('t16', 'PEDIDO', '2025-06-20', 'Dr. O', '2025-07-04', '2025-07-05', '14:00:00', '17:00:00', 'LARGE', 'HIGH', 'DELIVERED', '2'),
('t18', 'ENVIO', '2025-06-20', 'Dr. O', '2025-07-04', '2025-07-08', '14:00:00', '17:00:00', 'SMALL', 'MEDIUM', 'REJECTED', '4'),
('t19', 'PEDIDO', '2025-06-20', 'Camila Castro', '2025-07-03', '2025-07-08', '13:00:00', '16:00:00', 'MEDIUM', 'LOW', 'REJECTED', '1');

INSERT INTO transfers (
    id, type, request_date, requester, start_date, end_date,
    start_time, end_time, compartment, urgency, status,
    clinic_id, estimated_arrival_date
) VALUES
('t17', 'ENVIO', '2025-06-20', 'Omar Villadeamigo', '2025-07-04', '2025-07-08', '14:00:00', '17:00:00', 'SMALL', 'MEDIUM', 'DELIVERED', '1', '2025-07-05');


INSERT INTO supplies (id, name, weight, quantity, notes, transfer_id) VALUES
-- t1
('s1', 'Guantes', 1000, 5, 'Caja mediana', 't1'),
('s2', 'Vendas', 1200, 3, NULL, 't1'),

-- t2
('s3', 'Jeringas', 1500, 7, 'Caja grande', 't2'),
('s4', 'Gasas', 1300, 6, NULL, 't2'),

-- t3
('s5', 'Suero', 1000, 15, 'Frágil', 't3'),
('s6', 'Analgesicos', 1200, 2, NULL, 't3'),

-- t4
('s7', 'Alcohol', 1500, 4, NULL, 't4'),

-- t5
('s8', 'Mascarillas', 1300, 6, 'Uso urgente', 't5'),

-- t6
('s9', 'Antibióticos', 1200, 10, 'Caja sellada', 't6'),
('s10', 'Catéteres', 1500, 5, NULL, 't6'),

-- t7
('s11', 'Sueros grandes', 1300, 12, 'Frágil', 't7'),

-- t8
('s12', 'Gasas', 1400, 20, NULL, 't8'),

-- t9
('s13', 'Inyectables', 1500, 6, 'Refrigerar', 't9'),

-- t10
('s14', 'Material quirúrgico', 2800, 3, 'Alto costo', 't10'),

-- t11
('s15', 'Antisépticos', 1200, 10, 'Caja pequeña', 't11'),

-- t12
('s16', 'Antibióticos B', 1600, 8, 'Frágil', 't12'),

-- t13
('s17', 'Tijeras quirúrgicas', 2500, 2, 'Alto costo', 't13'),

-- t14
('s18', 'Solución fisiológica', 1000, 12, 'Mantener refrigerado', 't14'),
('s19', 'Oxígeno portátil', 1800, 1, 'Manipular con cuidado', 't14'),

-- t15
('s20', 'Mascarillas quirúrgicas', 1100, 20, NULL, 't15');


INSERT INTO rigi_routes (id, rigi_id, clinic_origin, clinic_destination, distance_km, flight_time_minutes) VALUES
(1, 1648, '0', '1', 32.13, '00:20'),
(2, 1610, '0', '2', 53.46, '00:32'),
(3, 1710, '0', '3', 21.41, '00:14'),
(9, 1899, '0', '4', 64.33, '00:38'),
(7, 1711, '0', '6', 51.31, '00:31'),
(6, 1690, '0', '7', 35.94, '00:22'),
(4, 1636, '1', '0', 32.15, '00:20'),
(5, 1649, '2', '0', 53.48, '00:32'),
(13, 1710, '3', '0', 21.41, '00:14'),
(10, 1914, '4', '0',  64.31, '00:38'),
(100, 1914, '4', '6',  64.31, '00:38'), -- no existe
(8, 1712, '6', '2', 20.63, '00:14'),
(80, 1712, '6', '4', 20.63, '00:14'), -- no existe
--(11, 2163, '7', '5', NULL, NULL),
(12, 3967, '7', '0', 35.94, '00:22');
