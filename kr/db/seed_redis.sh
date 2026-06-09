#!/bin/bash
# Скрипт для наполнения Redis тестовыми данными
# Ожидает, что redis-cli установлен или запускается внутри контейнера

echo "--- Наполнение Redis тестовыми данными ---"

# 1. Сессии пользователей (Key-Value)
# session_id -> user_id
redis-cli SET "session:token_abc123" "user_id_patient_1"
redis-cli SET "session:token_def456" "user_id_doctor_1"
redis-cli SET "session:token_ghi789" "user_id_admin_1"
redis-cli SET "session:token_jkl012" "user_id_patient_2"
redis-cli EXPIRE "session:token_abc123" 3600

# 2. Кэш расписания на сегодня (JSON-подобные строки)
# patient_id -> список лекарств на сегодня
redis-cli SET "patient:schedule:c5863bfb" '[{"drug": "Эналаприк", "time": "08:00", "dose": "5мг"}, {"drug": "Аспирин", "time": "12:00", "dose": "100мг"}]'
redis-cli SET "patient:schedule:a1b2c3d4" '[{"drug": "Метформин", "time": "09:00", "dose": "10мг"}]'
redis-cli SET "patient:schedule:f1e2d3c4" '[{"drug": "Эналаприк", "time": "08:00", "dose": "5мг"}, {"drug": "Лизиноприл", "time": "20:00", "dose": "10мг"}]'
redis-cli SET "patient:schedule:d9e8f7a6" '[{"drug": "Аспирин", "time": "10:00", "dose": "50мг"}]'

# 3. Очередь уведомлений (List)
# Добавляем уведомления в очередь
redis-cli LPUSH "notification:queue" "Reminder for patient c5863bfb: Take Эналаприк"
redis-cli LPUSH "notification:queue" "Reminder for patient a1b2c3d4: Take Метформин"
redis-cli LPUSH "notification:queue" "Reminder for patient f1e2d3c4: Take Эналаприк"
redis-cli LPUSH "notification:queue" "Reminder for patient d9e8f7a6: Take Аспирин"
redis-cli LPUSH "notification:queue" "System Alert: Schedule update for patient c5863bfb"

# 4. Быстрый справочник препаратов (Hashes)
# drug:info:ID -> {name: ..., unit: ...}
redis-cli HSET "drug:info:1" "name" "Эналаприк" "unit" "таб"
redis-cli HSET "drug:info:2" "name" "Метформин" "unit" "таб"
redis-cli HSET "drug:info:3" "name" "Аспирин" "unit" "таб"
redis-cli HSET "drug:info:4" "name" "Лизиноприл" "unit" "таб"
redis-cli HSET "drug:info:5" "name" "Амлодипин" "unit" "таб"

echo "--- Redis успешно наполнен! ---"