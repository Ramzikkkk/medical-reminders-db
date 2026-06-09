from medical_service import MedicalService
from repositories import PostgresRepository
import uuid

def run_demo():
    print("🚀 Starting Medical Reminders System Demo...")
    service = MedicalService()

    # Setup test data
    print("\n--- 1. Setup: Creating Test Data ---")
    # Create Doctor
    repo = PostgresRepository()
    with repo.get_cursor() as cur:
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) RETURNING user_id",
                    (f"doc_{uuid.uuid4().hex[:4]}", "hash", "Doctor"))
        u_id = cur.fetchone()['user_id']
        cur.execute("INSERT INTO doctors (user_id, specialization) VALUES (%s, %s) RETURNING doctor_id",
                    (u_id, "Cardiologist"))
        doc_id = cur.fetchone()['doctor_id']

        # Create a Drug
        cur.execute("INSERT INTO drugs_directory (trade_name, active_substance, unit) VALUES (%s, %s, %s) RETURNING drug_id",
                    ("Enalapril", "Enalaprilmaleate", "tab"))
        drug_id = cur.fetchone()['drug_id']

    # Create Patient
    p_id = service.create_patient("Ivan Ivanov", "1985-05-20")
    print(f"✅ Patient created: {p_id}")

    # Create Prescription
    pr_id = service.create_prescription(p_id, doc_id, "2026-06-01", "2026-07-01")
    print(f"✅ Prescription created: {pr_id}")

    # Add drug to prescription and create schedule
    with repo.get_cursor() as cur:
        cur.execute("INSERT INTO prescription_items (prescription_id, drug_id, dosage) VALUES (%s, %s, %s) RETURNING item_id",
                    (pr_id, drug_id, "5mg"))
        item_id = cur.fetchone()['item_id']
        cur.execute("INSERT INTO intake_schedules (item_id, time_of_day, days_of_week) VALUES (%s, %s, %s)",
                    (item_id, "08:00:00", "Mon,Wed,Fri"))
    print("✅ Drug and Schedule added to prescription")

    print("\n--- 2. Testing CRUD & JOINs ---")
    print("Listing prescriptions with Patient Names (JOIN):")
    prescs = service.list_prescriptions()
    for pr in prescs:
        if pr['prescription_id'] == pr_id:
            print(f"Prescription {pr['prescription_id']} belongs to Patient: {pr['patient_name']}")

    print("\n--- 3. Testing Redis (Sessions & Cache) ---")
    token = "demo_token_123"
    service.start_session(token, "user_ivan_123")
    print(f"Session created for token {token}. Verification: {service.check_session(token)}")

    service.cache_drug_info(drug_id, "Enalapril", "tab")
    print(f"Drug {drug_id} cached in Redis: {service.get_cached_drug(drug_id)}")

    print("\n--- 4. Testing Functional Reports ---")
    print("Report 1: Patient's Daily Schedule")
    schedule = service.get_patient_full_schedule(p_id)
    for s in schedule:
        print(f"💊 {s['trade_name']} | Time: {s['time_of_day']} | Dose: {s['dosage']}")

    print("\nReport 2: Drug Popularity (Enalapril)")
    pop = service.get_drug_popularity("Enalapril")
    print(f"Total patients taking Enalapril: {pop['patient_count']}")

    print("\n--- 5. Cleanup ---")
    service.delete_prescription(pr_id)
    service.delete_patient(p_id)
    service.end_session(token)
    print("✅ Demo cleanup completed.")

if __name__ == "__main__":
    run_demo()