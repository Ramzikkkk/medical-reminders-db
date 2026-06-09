from repositories import PatientRepository, PrescriptionRepository, SessionRepository, DrugCacheRepository

class MedicalService:
    def __init__(self):
        self.patients = PatientRepository()
        self.prescriptions = PrescriptionRepository()
        self.sessions = SessionRepository()
        self.drug_cache = DrugCacheRepository()

    # Patient Management
    def create_patient(self, name, birth_date):
        return self.patients.create(name, birth_date)

    def list_patients(self):
        return self.patients.get_all()

    def update_patient(self, p_id, name, birth_date):
        self.patients.update(p_id, name, birth_date)

    def delete_patient(self, p_id):
        self.patients.delete(p_id)

    # Prescription Management
    def create_prescription(self, p_id, d_id, start, end):
        return self.prescriptions.create(p_id, d_id, start, end)

    def list_prescriptions(self):
        return self.prescriptions.get_all_with_patients()

    def update_prescription(self, pr_id, start, end):
        self.prescriptions.update(pr_id, start, end)

    def delete_prescription(self, pr_id):
        self.prescriptions.delete(pr_id)

    # Redis Operations
    def start_session(self, token, user_id):
        self.sessions.create_session(token, user_id)

    def check_session(self, token):
        return self.sessions.get_session(token)

    def end_session(self, token):
        self.sessions.delete_session(token)

    def cache_drug_info(self, drug_id, name, unit):
        self.drug_cache.cache_drug(drug_id, name, unit)

    def get_cached_drug(self, drug_id):
        return self.drug_cache.get_drug(drug_id)

    # Functional Queries
    def get_patient_full_schedule(self, patient_id):
        return self.prescriptions.get_patient_schedule(patient_id)

    def get_drug_popularity(self, drug_name):
        return self.prescriptions.get_drug_statistics(drug_name)