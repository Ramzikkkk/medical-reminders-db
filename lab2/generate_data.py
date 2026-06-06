import csv
import uuid
import random
from datetime import datetime, timedelta

# Конфигурация
NUM_RECORDS = 60
DATA_DIR = 'lab2/data'

def random_date(start_year=1950, end_year=2023):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%Y-%m-%d')

def random_time():
    return f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00"

def generate_csv(filename, columns, data):
    with open(f"{DATA_DIR}/{filename}", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(data)

# Справочники
FIRST_NAMES = ["Иван", "Петр", "Сергей", "Алексей", "Дмитрий", "Андрей", "Максим", "Николай", "Михаил", "Артем"]
LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Попов", "Васильев", "Павлов", "Соколов", "Михайлов", "Новиков"]
PATRONYMICS = ["Иванович", "Петрович", "Сергеевич", "Алексеевич", "Дмитриевич", "Андреевич", "Максимович", "Николаевич", "Михайлович", "Артемьевич"]
SPECIALIZATIONS = ['Терапевт', 'Кардиолог', 'Эндокринолог', 'Невролог', 'Гастроэнтеролог', 'Офтальмолог']
DIAGNOSES = [("Гипертония", "Повышенное давление"), ("Диабет", "Нарушение обмена глюкозы"), ("Астигматизм", "Нарушение рефракции"), ("Гастрит", "Воспаление слизистой желудка"), ("Мигрень", "Сильные приступы головной боли")]
DRUGS = [("Эналаприл", "Эналаприлат", "таб"), ("Метформин", "Метформин", "таб"), ("Аспирин", "АЦС", "таб"), ("Омепразол", "Омепразол", "капс"), ("Лозартан", "Лозартан", "таб")]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 1. Users - гарантируем количество ролей
users_data = []
patient_user_ids = []
doctor_user_ids = []

for i in range(NUM_RECORDS):
    uid = str(uuid.uuid4())
    users_data.append([uid, f"patient_{i}", f"hash_{i}", 'Patient'])
    patient_user_ids.append(uid)

for i in range(NUM_RECORDS):
    uid = str(uuid.uuid4())
    users_data.append([uid, f"doctor_{i}", f"hash_{i+NUM_RECORDS}", 'Doctor'])
    doctor_user_ids.append(uid)

for i in range(5):
    uid = str(uuid.uuid4())
    users_data.append([uid, f"admin_{i}", f"hash_{i+2*NUM_RECORDS}", 'Admin'])

generate_csv('users.csv', ['user_id', 'username', 'password_hash', 'role'], users_data)

# 2. Patients
patient_ids = []
patients_data = []
for i in range(NUM_RECORDS):
    pid = str(uuid.uuid4())
    patient_ids.append(pid)
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)} {random.choice(PATRONYMICS)}"
    patients_data.append([pid, patient_user_ids[i], name, random_date(1940, 2010)])
generate_csv('patients.csv', ['patient_id', 'user_id', 'full_name', 'birth_date'], patients_data)

# 3. Doctors
doctor_ids = []
doctors_data = []
for i in range(NUM_RECORDS):
    did = str(uuid.uuid4())
    doctor_ids.append(did)
    doctors_data.append([did, doctor_user_ids[i], random.choice(SPECIALIZATIONS)])
generate_csv('doctors.csv', ['doctor_id', 'user_id', 'specialization'], doctors_data)

# 4. Diagnoses Directory
diag_ids = list(range(1, len(DIAGNOSES) + 1))
diag_data = [[i, DIAGNOSES[i-1][0], DIAGNOSES[i-1][1]] for i in diag_ids]
generate_csv('diagnoses_directory.csv', ['diag_id', 'name', 'description'], diag_data)

# 5. Patient Diagnoses
pdiag_data = []
for i in range(NUM_RECORDS * 2):
    pdiag_data.append([i+1, random.choice(patient_ids), random.choice(diag_ids), random_date(2010, 2023)])
generate_csv('patient_diagnoses.csv', ['id', 'patient_id', 'diag_id', 'detected_date'], pdiag_data)

# 6. Drugs Directory
drug_ids = list(range(1, len(DRUGS) + 1))
drug_data = [[i, DRUGS[i-1][0], DRUGS[i-1][1], DRUGS[i-1][2]] for i in drug_ids]
generate_csv('drugs_directory.csv', ['drug_id', 'trade_name', 'active_substance', 'unit'], drug_data)

# 7. Prescriptions
presc_ids = []
presc_data = []
for i in range(NUM_RECORDS * 2):
    pr_id = str(uuid.uuid4())
    presc_ids.append(pr_id)
    presc_data.append([pr_id, random.choice(patient_ids), random.choice(doctor_ids), random_date(2023, 2023), random_date(2023, 2024)])
generate_csv('prescriptions.csv', ['prescription_id', 'patient_id', 'doctor_id', 'start_date', 'end_date'], presc_data)

# 8. Prescription Items
items_ids = []
items_data = []
for pr_id in presc_ids:
    num_items = random.randint(1, 3)
    for _ in range(num_items):
        item_id = len(items_ids) + 1
        items_ids.append(item_id)
        items_data.append([item_id, pr_id, random.choice(drug_ids), f"{random.randint(1, 100)}мг"])
generate_csv('prescription_items.csv', ['item_id', 'prescription_id', 'drug_id', 'dosage'], items_data)

# 9. Intake Schedules
sched_ids = []
sched_data = []
for item_id in items_ids:
    num_times = random.randint(1, 3)
    for _ in range(num_times):
        s_id = len(sched_ids) + 1
        sched_ids.append(s_id)
        days = ",".join(random.sample(DAYS, random.randint(1, 7)))
        sched_data.append([s_id, item_id, random_time(), days])
generate_csv('intake_schedules.csv', ['schedule_id', 'item_id', 'time_of_day', 'days_of_week'], sched_data)

# 10. Intake Logs
logs_data = []
for s_id in sched_ids:
    for _ in range(random.randint(1, 5)):
        log_id = len(logs_data) + 1
        status = random.choice(['Taken', 'Skipped'])
        time = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S')
        logs_data.append([log_id, s_id, time, status])
generate_csv('intake_logs.csv', ['log_id', 'schedule_id', 'actual_time', 'status'], logs_data)