# Database configuration
import os

POSTGRES_CONFIG = {
    "dbname": "medical_reminders", # Replace with your actual DB name from lab1
    "user": "postgres",
    "password": "mysecretpassword", # Replace with your actual password
    "host": "localhost",
    "port": "5433"
}

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}