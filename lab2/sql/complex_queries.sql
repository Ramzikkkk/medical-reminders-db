-- Запрос 1: Пациенты, которым назначено более 2 препаратов (в разных назначениях)
-- Цель: Выявить пациентов с наиболее сложным курсом лечения.
SELECT p.full_name, COUNT(DISTINCT pr.prescription_id) as total_prescriptions
FROM patients p
JOIN prescriptions pr ON p.patient_id = pr.patient_id
GROUP BY p.patient_id, p.full_name
HAVING COUNT(DISTINCT pr.prescription_id) > 2;

-- Запрос 2: Статистика назначений по специализации врачей
-- Цель: Понять, какие специалисты назначают больше всего лекарств.
SELECT d.specialization, COUNT(pr.prescription_id) as total_prescriptions
FROM doctors d
JOIN prescriptions pr ON d.doctor_id = pr.doctor_id
GROUP BY d.specialization
ORDER BY total_prescriptions DESC;

-- Запрос 3: Поиск пациентов с конкретным диагнозом, принимающих конкретный препарат
-- Цель: Проверка соответствия лечения диагнозу (напр., Гипертония -> Эналаприл).
SELECT p.full_name, dd.name as diagnosis, dr.trade_name as drug
FROM patients p
JOIN patient_diagnoses pd ON p.patient_id = pd.patient_id
JOIN diagnoses_directory dd ON pd.diag_id = dd.diag_id
JOIN prescriptions pr ON p.patient_id = pr.patient_id
JOIN prescription_items pi ON pr.prescription_id = pi.prescription_id
JOIN drugs_directory dr ON pi.drug_id = dr.drug_id
WHERE dd.name = 'Гипертония' AND dr.trade_name = 'Эналаприл';

-- Запрос 4: Список всех приемов на сегодня (или за конкретный период) с именами пациентов
-- Цель: Формирование оперативного плана выдачи/приема лекарств.
SELECT p.full_name, dr.trade_name, s.time_of_day, pi.dosage
FROM patients p
JOIN prescriptions pr ON p.patient_id = pr.patient_id
JOIN prescription_items pi ON pr.prescription_id = pi.prescription_id
JOIN drugs_directory dr ON pi.drug_id = dr.drug_id
JOIN intake_schedules s ON pi.item_id = s.item_id
WHERE pr.start_date <= CURRENT_DATE AND (pr.end_date IS NULL OR pr.end_date >= CURRENT_DATE)
ORDER BY s.time_of_day;

-- Запрос 5: Анализ приверженности лечению (процент пропущенных приемов)
-- Цель: Найти пациентов, которые чаще всего пропускают прием лекарств.
SELECT p.full_name,
       ROUND(COUNT(CASE WHEN il.status = 'Skipped' THEN 1 END) * 100.0 / COUNT(*), 2) as skip_percentage
FROM patients p
JOIN prescriptions pr ON p.patient_id = pr.patient_id
JOIN prescription_items pi ON pr.prescription_id = pi.prescription_id
JOIN intake_schedules s ON pi.item_id = s.item_id
JOIN intake_logs il ON s.schedule_id = il.schedule_id
GROUP BY p.patient_id, p.full_name
HAVING COUNT(*) > 0
ORDER BY skip_percentage DESC;