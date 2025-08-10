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
('t1', 'ENVIO', '2025-07-08', 'Alex Romero', '2025-07-05', '2025-09-08', '10:00:00', '13:00:00', 'SMALL', 'LOW', 'PENDING', '1'),
('t2', 'PEDIDO', '2025-07-08', 'Dr. B', '2025-07-05', '2025-09-08', '11:30:00', '18:30:00', 'MEDIUM', 'MEDIUM', 'PENDING', '2'),
('t3', 'ENVIO', '2025-07-08', 'Dr. C', '2025-07-05', '2025-09-08', '09:00:00', '13:00:00', 'LARGE', 'HIGH', 'PENDING', '3'),
('t4', 'PEDIDO', '2025-07-08', 'Dr. D', '2025-07-05', '2025-09-08', '15:00:00', '17:00:00', 'SMALL', 'LOW', 'PENDING', '4'),
('t5', 'ENVIO', '2025-06-16', 'Dr. E', '2025-07-05', '2025-09-08', '14:00:00', '16:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '2'),
('t6', 'ENVIO', '2025-06-17', 'Dr. F', '2025-07-05', '2025-09-08', '08:00:00', '12:00:00', 'SMALL', 'LOW', 'PENDING', '4'),
('t7', 'PEDIDO', '2025-06-17', 'Dr. G', '2025-07-05', '2025-09-08', '10:30:00', '17:30:00', 'MEDIUM', 'MEDIUM', 'PENDING', '6'),
('t8', 'ENVIO', '2025-06-17', 'Julieta Sosa', '2025-07-03', '2025-09-08', '09:30:00', '15:00:00', 'LARGE', 'HIGH', 'PENDING', '1'),
('t9', 'PEDIDO', '2025-06-18', 'Dr. I', '2025-07-03', '2025-09-08', '14:00:00', '18:00:00', 'SMALL', 'LOW', 'PENDING', '3'),
('t10', 'ENVIO', '2025-06-18', 'Dr. J', '2025-07-05', '2025-09-08', '13:00:00', '16:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '4'),
('t11', 'ENVIO', '2025-06-18', 'Dr. K', '2025-07-05', '2025-09-08', '08:00:00', '11:00:00', 'SMALL', 'LOW', 'PENDING', '2'),
('t12', 'PEDIDO', '2025-06-19', 'Dr. L', '2025-07-05', '2025-09-08', '09:00:00', '12:00:00', 'MEDIUM', 'HIGH', 'PENDING', '3'),
('t13', 'ENVIO', '2025-06-19', 'Dr. M', '2025-07-04', '2025-09-08', '10:00:00', '14:00:00', 'LARGE', 'HIGH', 'PENDING', '4'),
('t14', 'PEDIDO', '2025-06-20', 'Dr. N', '2025-07-03', '2025-09-08', '13:00:00', '16:00:00', 'MEDIUM', 'LOW', 'PENDING', '3'),
('t15', 'ENVIO', '2025-06-20', 'Dr. O', '2025-07-04', '2025-09-08', '14:00:00', '17:00:00', 'SMALL', 'MEDIUM', 'PENDING', '6'),
('t16', 'PEDIDO', '2025-06-22', 'Dr. L', '2025-07-08', '2025-07-23', '07:00:00', '13:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '7'),
('t17', 'ENVIO', '2025-06-27', 'Dr. J', '2025-07-16', '2025-07-30', '08:00:00', '11:00:00', 'LARGE', 'MEDIUM', 'PENDING', '3'),
('t18', 'PEDIDO', '2025-06-19', 'Dr. J', '2025-07-04', '2025-07-15', '08:00:00', '10:00:00', 'SMALL', 'HIGH', 'PENDING', '4'),
('t19', 'PEDIDO', '2025-06-17', 'Dr. P', '2025-07-02', '2025-07-10', '14:00:00', '20:00:00', 'MEDIUM', 'HIGH', 'PENDING', '2'),
('t20', 'PEDIDO', '2025-06-25', 'Dr. K', '2025-07-11', '2025-07-19', '09:00:00', '13:00:00', 'MEDIUM', 'HIGH', 'PENDING', '2'),
('t21', 'ENVIO', '2025-06-20', 'Dr. L', '2025-07-05', '2025-07-16', '07:00:00', '11:00:00', 'LARGE', 'MEDIUM', 'PENDING', '6'),
('t22', 'ENVIO', '2025-06-23', 'Dr. K', '2025-07-09', '2025-07-17', '07:00:00', '09:00:00', 'LARGE', 'LOW', 'PENDING', '1'),
('t23', 'ENVIO', '2025-06-21', 'Dr. I', '2025-07-07', '2025-07-22', '14:00:00', '19:00:00', 'LARGE', 'MEDIUM', 'PENDING', '4'),
('t24', 'PEDIDO', '2025-06-21', 'Dr. M', '2025-07-10', '2025-07-25', '10:00:00', '13:00:00', 'MEDIUM', 'HIGH', 'PENDING', '6'),
('t25', 'ENVIO', '2025-06-25', 'Dr. M', '2025-07-12', '2025-07-27', '14:00:00', '20:00:00', 'MEDIUM', 'LOW', 'PENDING', '1'),
('t26', 'ENVIO', '2025-06-19', 'Dr. P', '2025-07-04', '2025-07-17', '09:00:00', '11:00:00', 'MEDIUM', 'LOW', 'PENDING', '7'),
('t27', 'PEDIDO', '2025-06-24', 'Dr. I', '2025-07-13', '2025-07-27', '12:00:00', '16:00:00', 'LARGE', 'LOW', 'PENDING', '4'),
('t28', 'PEDIDO', '2025-06-22', 'Dr. L', '2025-07-09', '2025-07-23', '07:00:00', '12:00:00', 'MEDIUM', 'LOW', 'PENDING', '7'),
('t29', 'PEDIDO', '2025-06-17', 'Dr. P', '2025-07-06', '2025-07-19', '14:00:00', '17:00:00', 'SMALL', 'MEDIUM', 'PENDING', '2'),
('t30', 'PEDIDO', '2025-06-23', 'Dr. M', '2025-07-13', '2025-07-27', '13:00:00', '16:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '1'),
('t31', 'PEDIDO', '2025-06-21', 'Dr. M', '2025-07-06', '2025-07-18', '11:00:00', '15:00:00', 'LARGE', 'MEDIUM', 'PENDING', '7'),
('t32', 'ENVIO', '2025-06-25', 'Dr. N', '2025-07-15', '2025-07-27', '11:00:00', '16:00:00', 'LARGE', 'MEDIUM', 'PENDING', '7'),
('t33', 'PEDIDO', '2025-06-24', 'Dr. J', '2025-07-11', '2025-07-19', '09:00:00', '15:00:00', 'LARGE', 'LOW', 'PENDING', '3'),
('t34', 'PEDIDO', '2025-06-23', 'Dr. K', '2025-07-10', '2025-07-21', '10:00:00', '15:00:00', 'SMALL', 'HIGH', 'PENDING', '1'),
('t35', 'PEDIDO', '2025-06-20', 'Dr. H', '2025-07-07', '2025-07-21', '11:00:00', '15:00:00', 'LARGE', 'MEDIUM', 'PENDING', '4'),
('t36', 'PEDIDO', '2025-06-26', 'Dr. L', '2025-07-13', '2025-07-26', '07:00:00', '13:00:00', 'SMALL', 'HIGH', 'PENDING', '6'),
('t37', 'ENVIO', '2025-06-19', 'Dr. N', '2025-07-06', '2025-07-20', '09:00:00', '15:00:00', 'SMALL', 'LOW', 'PENDING', '1'),
('t38', 'PEDIDO', '2025-06-27', 'Dr. N', '2025-07-17', '2025-08-01', '13:00:00', '18:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '2'),
('t39', 'ENVIO', '2025-06-27', 'Dr. L', '2025-07-12', '2025-07-24', '11:00:00', '16:00:00', 'LARGE', 'LOW', 'PENDING', '1'),
('t40', 'ENVIO', '2025-06-21', 'Dr. I', '2025-07-10', '2025-07-25', '08:00:00', '11:00:00', 'MEDIUM', 'LOW', 'PENDING', '3'),
('t41', 'PEDIDO', '2025-06-26', 'Dr. O', '2025-07-14', '2025-07-21', '11:00:00', '15:00:00', 'MEDIUM', 'LOW', 'PENDING', '6'),
('t42', 'ENVIO', '2025-06-19', 'Dr. K', '2025-07-07', '2025-07-21', '08:00:00', '10:00:00', 'SMALL', 'HIGH', 'PENDING', '1'),
('t43', 'PEDIDO', '2025-06-22', 'Dr. G', '2025-07-09', '2025-07-16', '14:00:00', '18:00:00', 'LARGE', 'HIGH', 'PENDING', '1'),
('t44', 'ENVIO', '2025-06-24', 'Dr. P', '2025-07-11', '2025-07-24', '12:00:00', '14:00:00', 'LARGE', 'HIGH', 'PENDING', '4'),
('t45', 'ENVIO', '2025-06-21', 'Dr. K', '2025-07-11', '2025-07-26', '07:00:00', '09:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '4'),
('t46', 'PEDIDO', '2025-06-27', 'Dr. K', '2025-07-15', '2025-07-22', '12:00:00', '18:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '1'),
('t47', 'PEDIDO', '2025-06-26', 'Dr. K', '2025-07-12', '2025-07-27', '14:00:00', '16:00:00', 'LARGE', 'MEDIUM', 'PENDING', '3'),
('t48', 'PEDIDO', '2025-06-20', 'Dr. O', '2025-07-08', '2025-07-20', '09:00:00', '14:00:00', 'MEDIUM', 'LOW', 'PENDING', '1'),
('t49', 'PEDIDO', '2025-06-17', 'Dr. K', '2025-07-07', '2025-07-17', '07:00:00', '12:00:00', 'LARGE', 'MEDIUM', 'PENDING', '1'),
('t50', 'ENVIO', '2025-06-22', 'Dr. L', '2025-07-08', '2025-07-19', '10:00:00', '14:00:00', 'SMALL', 'HIGH', 'PENDING', '1'),
('t51', 'PEDIDO', '2025-06-20', 'Dr. O', '2025-07-09', '2025-07-23', '07:00:00', '11:00:00', 'LARGE', 'MEDIUM', 'PENDING', '6'),
('t52', 'PEDIDO', '2025-06-27', 'Dr. O', '2025-07-13', '2025-07-27', '14:00:00', '19:00:00', 'MEDIUM', 'HIGH', 'PENDING', '2'),
('t53', 'ENVIO', '2025-06-17', 'Dr. P', '2025-07-04', '2025-07-15', '08:00:00', '14:00:00', 'MEDIUM', 'HIGH', 'PENDING', '4'),
('t54', 'ENVIO', '2025-06-26', 'Dr. P', '2025-07-14', '2025-07-22', '12:00:00', '14:00:00', 'MEDIUM', 'HIGH', 'PENDING', '3'),
('t55', 'PEDIDO', '2025-06-23', 'Dr. K', '2025-07-11', '2025-07-20', '08:00:00', '11:00:00', 'MEDIUM', 'LOW', 'PENDING', '7'),
('t56', 'ENVIO', '2025-06-23', 'Dr. P', '2025-07-09', '2025-07-21', '09:00:00', '13:00:00', 'SMALL', 'HIGH', 'PENDING', '2'),
('t57', 'ENVIO', '2025-06-19', 'Dr. K', '2025-07-06', '2025-07-18', '07:00:00', '11:00:00', 'MEDIUM', 'MEDIUM', 'PENDING', '3'),
('t58', 'ENVIO', '2025-06-27', 'Dr. H', '2025-07-17', '2025-08-01', '13:00:00', '19:00:00', 'LARGE', 'LOW', 'PENDING', '7'),
('t59', 'PEDIDO', '2025-06-21', 'Dr. G', '2025-07-11', '2025-07-26', '12:00:00', '15:00:00', 'LARGE', 'LOW', 'PENDING', '1'),
('t60', 'ENVIO', '2025-06-18', 'Dr. L', '2025-07-08', '2025-07-19', '13:00:00', '16:00:00', 'SMALL', 'LOW', 'PENDING', '1'),
('t61', 'ENVIO', '2025-06-26', 'Dr. K', '2025-07-11', '2025-07-25', '12:00:00', '17:00:00', 'MEDIUM', 'HIGH', 'PENDING', '3'),
('t62', 'ENVIO', '2025-06-25', 'Dr. N', '2025-07-12', '2025-07-27', '10:00:00', '14:00:00', 'LARGE', 'HIGH', 'PENDING', '6'),
('t63', 'PEDIDO', '2025-06-22', 'Dr. K', '2025-07-11', '2025-07-24', '13:00:00', '18:00:00', 'SMALL', 'LOW', 'PENDING', '1'),
('t64', 'PEDIDO', '2025-06-17', 'Dr. L', '2025-07-03', '2025-07-16', '07:00:00', '12:00:00', 'SMALL', 'LOW', 'PENDING', '2'),


('t180', 'ENVIO', '2025-06-20', 'Dr. O', '2025-07-04', '2025-07-08', '14:00:00', '17:00:00', 'SMALL', 'MEDIUM', 'REJECTED', '4'),
('t190', 'PEDIDO', '2025-06-20', 'Camila Castro', '2025-07-03', '2025-07-08', '13:00:00', '16:00:00', 'MEDIUM', 'LOW', 'REJECTED', '1');

INSERT INTO transfers (
    id, type, request_date, requester, start_date, end_date,
    start_time, end_time, compartment, urgency, status,
    clinic_id, estimated_arrival_date, estimated_arrival_time
) VALUES
-- ('t17', 'ENVIO', '2025-06-20', 'Omar Villadeamigo', '2025-07-04', '2025-07-08', '14:00:00', '17:00:00', 'SMALL', 'MEDIUM', 'DELIVERED', '1', '2025-07-05', null),
--('t20', 'PEDIDO', '2025-07-11', 'Mariana Bartesaghi', '2025-07-14', '2025-07-18', '09:00:00', '18:00:00', 'MEDIUM', 'MEDIUM', 'PLANNED', '1', '2025-07-14', '10:00:00'),
('t200', 'PEDIDO', '2025-07-11', 'Facundo Tessore', '2025-07-14', '2025-07-18', '09:00:00', '18:00:00', 'MEDIUM', 'MEDIUM', 'DELIVERED', '1', '2025-07-15', '10:00:00');
--('t16', 'PEDIDO', '2025-06-20', 'Guzmán Pintos', '2025-07-04', '2025-07-05', '14:00:00', '17:00:00', 'LARGE', 'HIGH', 'DELIVERED', '2', '2025-07-04', '10:00:00');
;


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
('s15', 'Material quirúrgico', 1221, 1, 'Caja pequeña', 't15'),
('s16', 'Tijeras quirúrgicas', 950, 9, 'Manipular con cuidado', 't15'),
('s17', 'Tijeras quirúrgicas', 1288, 10, 'Refrigerar', 't16'),
('s18', 'Tijeras quirúrgicas', 1167, 5, 'Manipular con cuidado', 't16'),
('s19', 'Inyectables', 1200, 12, 'Alto costo', 't17'),
('s20', 'Tijeras quirúrgicas', 1123, 1, 'Manipular con cuidado', 't18'),
('s21', 'Guantes', 1194, 5, 'Frágil', 't18'),
('s22', 'Guantes', 894, 6, 'Frágil', 't19'),
('s23', 'Inyectables', 1247, 4, 'Mantener refrigerado', 't19'),
('s24', 'Guantes', 1065, 9, 'Manipular con cuidado', 't20'),
('s25', 'Tijeras quirúrgicas', 1163, 14, 'Manipular con cuidado', 't20'),
('s26', 'Guantes', 1098, 4, 'Mantener refrigerado', 't21'),
('s27', 'Tijeras quirúrgicas', 1211, 13, 'Manipular con cuidado', 't21'),
('s28', 'Jeringas', 1012, 7, 'Frágil', 't22'),
('s29', 'Solución fisiológica', 1111, 5, 'Caja pequeña', 't22'),
('s30', 'Tijeras quirúrgicas', 1277, 8, 'Manipular con cuidado', 't23'),
('s31', 'Material quirúrgico', 1074, 5, 'Mantener refrigerado', 't24'),
('s32', 'Guantes', 1022, 4, 'Manipular con cuidado', 't25'),
('s33', 'Jeringas', 894, 11, 'Frágil', 't25'),
('s34', 'Material quirúrgico', 1168, 10, 'Caja pequeña', 't26'),
('s35', 'Inyectables', 1127, 1, 'Caja pequeña', 't26'),
('s36', 'Material quirúrgico', 1103, 2, 'Alto costo', 't27'),
('s37', 'Oxígeno portátil', 1185, 2, 'Frágil', 't28'),
('s38', 'Vendajes', 1049, 5, 'Alto costo', 't28'),
('s39', 'Inyectables', 981, 12, 'Manipular con cuidado', 't29'),
('s40', 'Antibióticos B', 1234, 13, 'Manipular con cuidado', 't30'),
('s41', 'Solución fisiológica', 1176, 2, 'Manipular con cuidado', 't30'),
('s42', 'Oxígeno portátil', 1148, 11, 'Frágil', 't31'),
('s43', 'Material quirúrgico', 937, 15, 'Caja pequeña', 't31'),
('s44', 'Vendajes', 1090, 10, 'Manipular con cuidado', 't32'),
('s45', 'Oxígeno portátil', 1282, 9, 'Refrigerar', 't32'),
('s46', 'Antisépticos', 1220, 3, 'Frágil', 't33'),
('s47', 'Jeringas', 1198, 5, 'Refrigerar', 't34'),
('s48', 'Oxígeno portátil', 1016, 12, 'Mantener refrigerado', 't34'),
('s49', 'Tijeras quirúrgicas', 1094, 11, 'Frágil', 't35'),
('s50', 'Antibióticos B', 1025, 9, 'Caja pequeña', 't35'),
('s51', 'Jeringas', 1175, 8, 'Manipular con cuidado', 't36'),
('s52', 'Solución fisiológica', 1255, 11, 'Manipular con cuidado', 't37'),
('s53', 'Material quirúrgico', 989, 9, 'Alto costo', 't37'),
('s54', 'Guantes', 951, 12, 'Manipular con cuidado', 't38'),
('s55', 'Guantes', 1232, 1, 'Refrigerar', 't38'),
('s56', 'Solución fisiológica', 1066, 14, 'Mantener refrigerado', 't39'),
('s57', 'Antisépticos', 936, 4, 'Frágil', 't40'),
('s58', 'Guantes', 1099, 13, 'Alto costo', 't41'),
('s59', 'Tijeras quirúrgicas', 982, 15, 'Frágil', 't41'),
('s60', 'Jeringas', 964, 3, 'Alto costo', 't42'),
('s61', 'Guantes', 1033, 8, 'Mantener refrigerado', 't43'),
('s62', 'Oxígeno portátil', 1186, 8, 'Mantener refrigerado', 't44'),
('s63', 'Antisépticos', 1224, 2, 'Refrigerar', 't44'),
('s64', 'Inyectables', 1031, 6, 'Frágil', 't45'),
('s65', 'Antibióticos B', 1093, 6, 'Alto costo', 't46'),
('s66', 'Tijeras quirúrgicas', 1161, 15, 'Frágil', 't46'),
('s67', 'Inyectables', 1128, 8, 'Refrigerar', 't47'),
('s68', 'Vendajes', 1230, 2, 'Frágil', 't48'),
('s69', 'Jeringas', 989, 10, 'Mantener refrigerado', 't48'),
('s70', 'Jeringas', 1274, 4, 'Alto costo', 't49'),
('s71', 'Material quirúrgico', 1242, 10, 'Refrigerar', 't49'),
('s72', 'Material quirúrgico', 1160, 2, 'Manipular con cuidado', 't50'),
('s73', 'Solución fisiológica', 1017, 8, 'Mantener refrigerado', 't51'),
('s74', 'Guantes', 1044, 13, 'Mantener refrigerado', 't52'),
('s75', 'Solución fisiológica', 1085, 13, 'Caja pequeña', 't53'),
('s76', 'Vendajes', 1215, 12, 'Frágil', 't53'),
('s77', 'Tijeras quirúrgicas', 913, 13, 'Mantener refrigerado', 't54'),
('s78', 'Solución fisiológica', 1229, 12, 'Refrigerar', 't54'),
('s79', 'Tijeras quirúrgicas', 1194, 6, 'Mantener refrigerado', 't55'),
('s80', 'Solución fisiológica', 1232, 7, 'Mantener refrigerado', 't56'),
('s81', 'Jeringas', 1266, 2, 'Refrigerar', 't57'),
('s82', 'Tijeras quirúrgicas', 1101, 4, 'Alto costo', 't57'),
('s83', 'Vendajes', 1010, 1, 'Caja pequeña', 't58'),
('s84', 'Material quirúrgico', 1224, 10, 'Refrigerar', 't58'),
('s85', 'Material quirúrgico', 1168, 6, 'Caja pequeña', 't59'),
('s86', 'Material quirúrgico', 1273, 10, 'Mantener refrigerado', 't59'),
('s87', 'Jeringas', 1204, 12, 'Caja pequeña', 't60'),
('s88', 'Inyectables', 1197, 14, 'Manipular con cuidado', 't61'),
('s89', 'Inyectables', 1212, 6, 'Refrigerar', 't62'),
('s90', 'Vendajes', 1128, 9, 'Caja pequeña', 't62'),
('s91', 'Oxígeno portátil', 1120, 8, 'Alto costo', 't63'),
('s92', 'Antisépticos', 1095, 15, 'Frágil', 't64');


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
(90, 1712, '2', '6', 20.63, '00:14'),
(80, 1712, '6', '4', 20.63, '00:14'), -- no existe
--(11, 2163, '7', '5', NULL, NULL),
(12, 3967, '7', '0', 35.94, '00:22'),
(91, 1711, '6', '0', 51.31, '00:31');
