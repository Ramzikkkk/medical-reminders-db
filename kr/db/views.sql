-- Представления (Views)

-- 1. Расписание приемов на день для всех пациентов
-- Объединяет данные о пациенте, препарате, дозировке и времени приема.
CREATE OR REPLACE VIEW v_patient_daily_schedule AS
SELECT
    p.full_name AS patient_name,
    dr.trade_name AS medication,
    pi.dosage,
    s.time_of_day,
    s.days_of_week
FROM patients p
JOIN prescriptions pr ON p.patient_id = pr.patient_id
JOIN prescription_items pi ON pr.prescription_id = pi.prescription_id
JOIN drugs_directory dr ON pi.drug_id = dr.drug_id
JOIN intake_schedules s ON pi.item_id = s.item_id
WHERE pr.start_date <= CURRENT_DATE
  AND (pr.end_date IS NULL OR pr.end_date >= CURRENT_DATE);

-- 2. Загруженность врачей
-- Показывает, сколько пациентов прикреплено к каждому врачу и общее число назначений.
CREATE OR REPLACE VIEW v_doctor_workload AS
SELECT
    d.specialization,
    d.doctor_id,
    COUNT(DISTINCT pr.patient_id) as unique_patients,
    COUNT(pr.prescription_id) as total_prescriptions
FROM doctors d
LEFT JOIN prescriptions pr ON d.doctor_id = pr.doctor_id
GROUP BY d.doctor_id, d.specialization;

-- Тесты VIEW
-- SELECT * FROM v_patient_daily_schedule LIMIT 10;
-- SELECT * FROM v_doctor_workload;