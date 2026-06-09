-- Наполнение справочников и пользователей
INSERT INTO users (username, password_hash, role) VALUES
('dr_smith', 'hash1', 'Doctor'),
('patient_ivan', 'hash2', 'Patient'),
('admin_main', 'hash3', 'Admin');

-- Наполнение пациентов и врачей (используем подзапросы для получения UUID)
INSERT INTO patients (user_id, full_name, birth_date)
VALUES ((SELECT user_id FROM users WHERE username = 'patient_ivan'), 'Иванов Иван Иванович', '1985-05-20');

INSERT INTO doctors (user_id, specialization)
VALUES ((SELECT user_id FROM users WHERE username = 'dr_smith'), 'Терапевт');

-- Справочник диагнозов
INSERT INTO diagnoses_directory (name, description) VALUES
('Гипертония', 'Повышенное артериальное давление'),
('Сахарный диабет 2 типа', 'Нарушение обмена глюкозы');

-- Привязка диагноза к пациенту
INSERT INTO patient_diagnoses (patient_id, diag_id, detected_date)
VALUES ((SELECT patient_id FROM patients WHERE full_name = 'Иванов Иван Иванович'), 1, '2023-01-10');

-- Справочник препаратов
INSERT INTO drugs_directory (trade_name, active_substance, unit) VALUES
('Эналаприк', 'Эналаприлат', 'таб'),
('Метформин', 'Метформин', 'таб'),
('Аспирин', 'Ацетилсалициловая кислота', 'таб');


-- Создание назначения
INSERT INTO prescriptions (patient_id, doctor_id, start_date, end_date)
VALUES (
    (SELECT patient_id FROM patients WHERE full_name = 'Иванов Иван Иванович'),
    (SELECT doctor_id FROM doctors WHERE specialization = 'Терапевт'),
    '2023-10-01', '2023-11-01'
);

-- Добавление препаратов в назначение
INSERT INTO prescription_items (prescription_id, drug_id, dosage)
VALUES
((SELECT prescription_id FROM prescriptions LIMIT 1), 1, '5мг'),
((SELECT prescription_id FROM prescriptions LIMIT 1), 3, '100мг');

-- Настройка графика приема (например, Эналаприк утром и вечером)
INSERT INTO intake_schedules (item_id, time_of_day, days_of_week)
VALUES
(1, '08:00:00', 'Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
(1, '20:00:00', 'Mon,Tue,Wed,Thu,Fri,Sat,Sun'),
(2, '12:00:00', 'Mon,Wed,Fri');

-- Тестовые логи приемов
INSERT INTO intake_logs (schedule_id, actual_time, status) VALUES
(1, CURRENT_TIMESTAMP - INTERVAL '1 day', 'Taken'),
(2, CURRENT_TIMESTAMP - INTERVAL '1 day', 'Skipped');