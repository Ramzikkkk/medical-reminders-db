-- Функции

-- 1. Функция для подсчета общего количества приемов препаратов за сутки для пациента
CREATE OR REPLACE FUNCTION get_daily_pill_count(p_id UUID)
RETURNS INTEGER AS $$
DECLARE
    total_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_count
    FROM prescriptions pr
    JOIN prescription_items pi ON pr.prescription_id = pi.prescription_id
    JOIN intake_schedules s ON pi.item_id = s.item_id
    WHERE pr.patient_id = p_id
      AND pr.start_date <= CURRENT_DATE
      AND (pr.end_date IS NULL OR pr.end_date >= CURRENT_DATE);

    RETURN total_count;
END;
$$ LANGUAGE plpgsql;

-- 2. Функция проверки активности назначения
CREATE OR REPLACE FUNCTION is_prescription_active(pr_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    is_active BOOLEAN;
BEGIN
    SELECT (start_date <= CURRENT_DATE AND (end_date IS NULL OR end_date >= CURRENT_DATE))
    INTO is_active
    FROM prescriptions
    WHERE prescription_id = pr_id;

    RETURN COALESCE(is_active, FALSE);
END;
$$ LANGUAGE plpgsql;

-- Процедуры

-- 1. Процедура добавления препарата в назначение с проверкой
CREATE OR REPLACE PROCEDURE add_drug_to_prescription(
    p_presc_id UUID,
    p_drug_id INTEGER,
    p_dosage VARCHAR
)
AS $$
BEGIN
    -- Проверка существования препарата
    IF NOT EXISTS (SELECT 1 FROM drugs_directory WHERE drug_id = p_drug_id) THEN
        RAISE EXCEPTION 'Препарат с ID % не найден в справочнике', p_drug_id;
    END IF;

    INSERT INTO prescription_items (prescription_id, drug_id, dosage)
    VALUES (p_presc_id, p_drug_id, p_dosage);
END;
$$ LANGUAGE plpgsql;

-- 2. Процедура массовой отметки приемов как "Принято" для конкретного пациента
CREATE OR REPLACE PROCEDURE mark_all_as_taken(p_id UUID)
AS $$
BEGIN
    INSERT INTO intake_logs (schedule_id, actual_time, status)
    SELECT s.schedule_id, CURRENT_TIMESTAMP, 'Taken'
    FROM prescriptions pr
    JOIN prescription_items pi ON pr.prescription_id = pi.prescription_id
    JOIN intake_schedules s ON pi.item_id = s.item_id
    WHERE pr.patient_id = p_id
      AND pr.start_date <= CURRENT_DATE
      AND (pr.end_date IS NULL OR pr.end_date >= CURRENT_DATE);
END;
$$ LANGUAGE plpgsql;

-- Тесты
-- SELECT get_daily_pill_count((SELECT patient_id FROM patients LIMIT 1));
-- SELECT is_prescription_active((SELECT prescription_id FROM prescriptions LIMIT 1));
-- CALL add_drug_to_prescription((SELECT prescription_id FROM prescriptions LIMIT 1), 1, '10мг');
-- CALL mark_all_as_taken((SELECT patient_id FROM patients LIMIT 1));