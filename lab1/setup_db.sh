#!/bin/bash

# Настройки
DB_NAME="medical_reminders"
PG_USER="postgres" # Замени на своего пользователя, если отличается

echo "--- Запуск процесса инициализации БД ---"

# 1. Создание базы данных
echo "Создание базы данных $DB_NAME..."
psql -U $PG_USER -c "CREATE DATABASE $DB_NAME;" || echo "База данных уже существует или ошибка при создании."

# 2. Создание структуры (Таблицы)
echo "Применение схемы из init_db.sql..."
psql -U $PG_USER -d $DB_NAME -f init_db.sql

# 3. Наполнение данными
echo "Заполнение данными из seed_data.sql..."
psql -U $PG_USER -d $DB_NAME -f seed_data.sql

echo "--- Готово! Теперь можно подключаться через DBeaver к базе $DB_NAME ---"