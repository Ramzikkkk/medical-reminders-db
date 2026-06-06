CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('Patient', 'Doctor', 'Admin'))
);

CREATE TABLE patients (
    patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(user_id),
    full_name VARCHAR(255) NOT NULL,
    birth_date DATE
);

CREATE TABLE doctors (
    doctor_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(user_id),
    specialization VARCHAR(100)
);

CREATE TABLE diagnoses_directory (
    diag_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE patient_diagnoses (
    id SERIAL PRIMARY KEY,
    patient_id UUID REFERENCES patients(patient_id),
    diag_id INT REFERENCES diagnoses_directory(diag_id),
    detected_date DATE
);

CREATE TABLE drugs_directory (
    drug_id SERIAL PRIMARY KEY,
    trade_name VARCHAR(255) NOT NULL,
    active_substance VARCHAR(255),
    unit VARCHAR(50)
);

CREATE TABLE prescriptions (
    prescription_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id),
    doctor_id UUID REFERENCES doctors(doctor_id),
    start_date DATE NOT NULL,
    end_date DATE
);

CREATE TABLE prescription_items (
    item_id SERIAL PRIMARY KEY,
    prescription_id UUID REFERENCES prescriptions(prescription_id),
    drug_id INT REFERENCES drugs_directory(drug_id),
    dosage VARCHAR(50)
);

CREATE TABLE intake_schedules (
    schedule_id SERIAL PRIMARY KEY,
    item_id INT REFERENCES prescription_items(item_id),
    time_of_day TIME NOT NULL,
    days_of_week VARCHAR(100)
);

CREATE TABLE intake_logs (
    log_id BIGSERIAL PRIMARY KEY,
    schedule_id INT REFERENCES intake_schedules(schedule_id),
    actual_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('Taken', 'Skipped'))
);