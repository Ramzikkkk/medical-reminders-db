from medical_service import MedicalService
import uuid

def test_app():
    print("Starting verification tests...")
    service = MedicalService()
    p_id = None
    pr_id = None

    try:
        # 1. Test Patient CRUD
        print("Testing Patient CRUD...")
        p_id = service.create_patient("Test User", "1990-01-01")
        print(f"Created patient: {p_id}")
        patients = service.list_patients()
        print(f"Total patients: {len(patients)}")
        service.update_patient(p_id, "Updated Test User", "1990-01-01")
        print("Patient updated.")

        # 2. Test Prescription CRUD (with JOIN)
        print("\nTesting Prescription CRUD...")

        # Create a doctor first to avoid FK violation
        from repositories import PostgresRepository
        repo = PostgresRepository()
        with repo.get_cursor() as cur:
            # Create a user for the doctor
            cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) RETURNING user_id",
                        (f"test_doc_{uuid.uuid4().hex[:6]}", "hash", "Doctor"))
            u_id = cur.fetchone()['user_id']
            # Create the doctor
            cur.execute("INSERT INTO doctors (user_id, specialization) VALUES (%s, %s) RETURNING doctor_id",
                        (u_id, "General Practitioner"))
            d_id = cur.fetchone()['doctor_id']
            print(f"Created test doctor: {d_id}")

        pr_id = service.create_prescription(p_id, d_id, "2026-06-01", "2026-06-30")
        print(f"Created prescription: {pr_id}")

        prescs = service.list_prescriptions()
        print(f"Total prescriptions: {len(prescs)}")
        # Verify JOIN: the list should have 'patient_name'
        if prescs and 'patient_name' in prescs[0]:
            print("JOIN check passed: patient_name found.")

        # 3. Test Redis CRUD
        print("\nTesting Redis CRUD...")
        service.start_session("test_token", "user_123")
        uid = service.check_session("test_token")
        print(f"Session retrieved: {uid}")
        service.cache_drug_info("101", "TestDrug", "tabs")
        drug = service.get_cached_drug("101")
        print(f"Drug retrieved from cache: {drug}")

        # 4. Test Functional Queries
        print("\nTesting Functional Queries...")
        schedule = service.get_patient_full_schedule(p_id)
        print(f"Schedule count: {len(schedule)}")

        pop = service.get_drug_popularity("Test")
        print(f"Popularity: {pop['patient_count']}")

        print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nCleaning up...")
        if pr_id:
            try: service.delete_prescription(pr_id)
            except: pass
        if p_id:
            try: service.delete_patient(p_id)
            except: pass
        try: service.end_session("test_token")
        except: pass
        print("Cleanup finished.")

if __name__ == "__main__":
    test_app()