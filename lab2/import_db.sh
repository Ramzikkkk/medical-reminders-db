#!/bin/bash

# Конфигурация
CONTAINER_NAME="medical_db_postgres"
DB_NAME="medical_reminders"
DB_USER="postgres"
DATA_DIR="lab2/data"

echo "Cleaning existing data..."
docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "TRUNCATE users, patients, doctors, diagnoses_directory, patient_diagnoses, drugs_directory, prescriptions, prescription_items, intake_schedules, intake_logs CASCADE;"

echo "Importing CSV files..."

# Порядок импорта важен из-за Foreign Keys
TABLES=(
    "users"
    "patients"
    "doctors"
    "diagnoses_directory"
    "patient_diagnoses"
    "drugs_directory"
    "prescriptions"
    "prescription_items"
    "intake_schedules"
    "intake_logs"
)

for TABLE in "${TABLES[@]}"; do
    echo "Importing $TABLE..."
    cat "$DATA_DIR/$TABLE.csv" | docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "COPY $TABLE FROM stdin WITH (FORMAT csv, HEADER true, ENCODING 'utf8');"
done

echo "Data import completed successfully!"