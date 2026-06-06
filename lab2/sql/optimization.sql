-- Оптимизация Запроса 3: Поиск по названиям диагноза и препарата
CREATE INDEX idx_diag_name ON diagnoses_directory(name);
CREATE INDEX idx_drug_trade_name ON drugs_directory(trade_name);

-- Оптимизация Запроса 4: Фильтрация по датам назначений
CREATE INDEX idx_prescriptions_dates ON prescriptions(start_date, end_date);

-- Оптимизация Запроса 5: Фильтрация и группировка по статусам логов и связям
CREATE INDEX idx_intake_logs_status ON intake_logs(status);
CREATE INDEX idx_intake_logs_sched_id ON intake_logs(schedule_id);
CREATE INDEX idx_presc_items_presc_id ON prescription_items(prescription_id);