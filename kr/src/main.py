import sys
from medical_service import MedicalService

def print_header(text):
    print(f"\n{'='*50}\n{text.center(50)}\n{'='*50}")

def main():
    service = MedicalService()

    while True:
        print_header("Medical Reminders System - Admin Panel")
        print("1. 👥 Patients Management")
        print("2. 💊 Prescriptions Management")
        print("3. 🔑 Session & Cache (Redis)")
        print("4. 📊 Functional Reports")
        print("0. ❌ Exit")

        choice = input("\nSelect an option: ")

        if choice == '0':
            print("Exiting... Goodbye!")
            break

        elif choice == '1':
            patient_menu(service)
        elif choice == '2':
            prescription_menu(service)
        elif choice == '3':
            redis_menu(service)
        elif choice == '4':
            reports_menu(service)
        else:
            print("Invalid choice, try again.")

def patient_menu(service):
    while True:
        print_header("Patients Management")
        print("1. List all patients")
        print("2. Add new patient")
        print("3. Update patient")
        print("4. Delete patient")
        print("0. Back")

        choice = input("\nOption: ")
        if choice == '0': break

        if choice == '1':
            patients = service.list_patients()
            print("\n--- Patient List ---")
            for p in patients:
                print(f"ID: {p['patient_id']} | Name: {p['full_name']} | Birth: {p['birth_date']}")
        elif choice == '2':
            name = input("Full Name: ")
            date = input("Birth Date (YYYY-MM-DD): ")
            p_id = service.create_patient(name, date)
            print(f"Patient created with ID: {p_id}")
        elif choice == '3':
            p_id = input("Patient ID to update: ")
            name = input("New Name: ")
            date = input("New Birth Date (YYYY-MM-DD): ")
            service.update_patient(p_id, name, date)
            print("Patient updated.")
        elif choice == '4':
            p_id = input("Patient ID to delete: ")
            service.delete_patient(p_id)
            print("Patient deleted.")

def prescription_menu(service):
    while True:
        print_header("Prescriptions Management")
        print("1. List all prescriptions (with Patients)")
        print("2. Create prescription")
        print("3. Update prescription")
        print("4. Delete prescription")
        print("0. Back")

        choice = input("\nOption: ")
        if choice == '0': break

        if choice == '1':
            prescs = service.list_prescriptions()
            print("\n--- Prescriptions ---")
            for pr in prescs:
                print(f"ID: {pr['prescription_id']} | Patient: {pr['patient_name']} | From: {pr['start_date']} To: {pr['end_date']}")
        elif choice == '2':
            p_id = input("Patient ID: ")
            d_id = input("Doctor ID: ")
            start = input("Start Date (YYYY-MM-DD): ")
            end = input("End Date (YYYY-MM-DD): ")
            pr_id = service.create_prescription(p_id, d_id, start, end)
            print(f"Prescription created with ID: {pr_id}")
        elif choice == '3':
            pr_id = input("Prescription ID: ")
            start = input("New Start Date: ")
            end = input("New End Date: ")
            service.update_prescription(pr_id, start, end)
            print("Prescription updated.")
        elif choice == '4':
            pr_id = input("Prescription ID: ")
            service.delete_prescription(pr_id)
            print("Prescription deleted.")

def redis_menu(service):
    while True:
        print_header("Redis Session & Cache")
        print("1. Create Session")
        print("2. Check Session")
        print("3. Delete Session")
        print("4. Cache Drug Info")
        print("5. Get Cached Drug")
        print("0. Back")

        choice = input("\nOption: ")
        if choice == '0': break

        if choice == '1':
            token = input("Token: ")
            u_id = input("User ID: ")
            service.start_session(token, u_id)
            print("Session started.")
        elif choice == '2':
            token = input("Token: ")
            uid = service.check_session(token)
            print(f"Session belongs to User: {uid}" if uid else "Session not found.")
        elif choice == '3':
            token = input("Token: ")
            service.end_session(token)
            print("Session ended.")
        elif choice == '4':
            d_id = input("Drug ID: ")
            name = input("Drug Name: ")
            unit = input("Unit: ")
            service.cache_drug_info(d_id, name, unit)
            print("Drug cached.")
        elif choice == '5':
            d_id = input("Drug ID: ")
            drug = service.get_cached_drug(d_id)
            print(f"Drug Info: {drug}" if drug else "Not in cache.")

def reports_menu(service):
    while True:
        print_header("Functional Reports")
        print("1. Patient's Daily Schedule")
        print("2. Drug Popularity Statistics")
        print("0. Back")

        choice = input("\nOption: ")
        if choice == '0': break

        if choice == '1':
            p_id = input("Patient ID: ")
            schedule = service.get_patient_full_schedule(p_id)
            print(f"\n--- Schedule for Patient {p_id} ---")
            if not schedule:
                print("No entries found.")
            for item in schedule:
                print(f"💊 {item['trade_name']} | Time: {item['time_of_day']} | Dose: {item['dosage']}")
        elif choice == '2':
            drug = input("Drug Name (partial search): ")
            stat = service.get_drug_popularity(drug)
            print(f"\n📈 Total patients taking {drug}: {stat['patient_count']}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nForced exit.")
        sys.exit(0)