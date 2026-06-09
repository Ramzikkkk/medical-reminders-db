import psycopg2
from psycopg2 import extras
import redis
from db_config import POSTGRES_CONFIG, REDIS_CONFIG

class PostgresRepository:
    def __init__(self):
        self.conn = psycopg2.connect(**POSTGRES_CONFIG)
        self.conn.autocommit = True

    def get_cursor(self):
        return self.conn.cursor(cursor_factory=extras.RealDictCursor)

class PatientRepository(PostgresRepository):
    def create(self, full_name, birth_date):
        with self.get_cursor() as cur:
            cur.execute(
                "INSERT INTO patients (full_name, birth_date) VALUES (%s, %s) RETURNING patient_id",
                (full_name, birth_date)
            )
            return cur.fetchone()['patient_id']

    def get_all(self):
        with self.get_cursor() as cur:
            cur.execute("SELECT * FROM patients")
            return cur.fetchall()

    def get_by_id(self, patient_id):
        with self.get_cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            return cur.fetchone()

    def update(self, patient_id, full_name, birth_date):
        with self.get_cursor() as cur:
            cur.execute(
                "UPDATE patients SET full_name = %s, birth_date = %s WHERE patient_id = %s",
                (full_name, birth_date, patient_id)
            )

    def delete(self, patient_id):
        with self.get_cursor() as cur:
            cur.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))

class PrescriptionRepository(PostgresRepository):
    def create(self, patient_id, doctor_id, start_date, end_date):
        with self.get_cursor() as cur:
            cur.execute(
                "INSERT INTO prescriptions (patient_id, doctor_id, start_date, end_date) VALUES (%s, %s, %s, %s) RETURNING prescription_id",
                (patient_id, doctor_id, start_date, end_date)
            )
            return cur.fetchone()['prescription_id']

    def get_all_with_patients(self):
        # Requirement 7: JOIN to show attributes instead of IDs
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT pr.prescription_id, p.full_name as patient_name, pr.start_date, pr.end_date
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
            """)
            return cur.fetchall()

    def update(self, prescription_id, start_date, end_date):
        with self.get_cursor() as cur:
            cur.execute(
                "UPDATE prescriptions SET start_date = %s, end_date = %s WHERE prescription_id = %s",
                (start_date, end_date, prescription_id)
            )

    def delete(self, prescription_id):
        with self.get_cursor() as cur:
            cur.execute("DELETE FROM prescriptions WHERE prescription_id = %s", (prescription_id,))

    # Functional Queries
    def get_patient_schedule(self, patient_id):
        # Requirement 8: Functional query 1
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT d.trade_name, s.time_of_day, pi.dosage
                FROM patients p
                JOIN prescriptions pr ON p.patient_id = pr.patient_id
                JOIN prescription_items pi ON pr.prescription_id = pi.prescription_id
                JOIN drugs_directory d ON pi.drug_id = d.drug_id
                JOIN intake_schedules s ON pi.item_id = s.item_id
                WHERE p.patient_id = %s
            """, (patient_id,))
            return cur.fetchall()

    def get_drug_statistics(self, drug_name):
        # Requirement 8: Functional query 2
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT COUNT(DISTINCT pr.patient_id) as patient_count
                FROM drugs_directory d
                JOIN prescription_items pi ON d.drug_id = pi.drug_id
                JOIN prescriptions pr ON pi.prescription_id = pr.prescription_id
                WHERE d.trade_name ILIKE %s
            """, (f"%{drug_name}%",))
            return cur.fetchone()

class RedisRepository:
    def __init__(self):
        self.client = redis.Redis(**REDIS_CONFIG, decode_responses=True)

class SessionRepository(RedisRepository):
    def create_session(self, token, user_id, expires=3600):
        self.client.setex(f"session:{token}", expires, user_id)

    def get_session(self, token):
        return self.client.get(f"session:{token}")

    def delete_session(self, token):
        return self.client.delete(f"session:{token}")

class DrugCacheRepository(RedisRepository):
    def cache_drug(self, drug_id, name, unit):
        self.client.hset(f"drug:info:{drug_id}", mapping={"name": name, "unit": unit})

    def get_drug(self, drug_id):
        return self.client.hgetall(f"drug:info:{drug_id}")

    def delete_drug(self, drug_id):
        return self.client.delete(f"drug:info:{drug_id}")