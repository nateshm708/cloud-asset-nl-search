import sqlite3
import os

DB_PATH = os.path.join("data", "cloud_inventory.db")
SCHEMA_PATH = os.path.join("db", "schema.sql")
SEED_PATH = os.path.join("db", "seed_data.sql")

def initialize_database():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute Schema
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    print("Database tables created successfully.")

    # Execute Seed Data
    with open(SEED_PATH, "r") as f:
        seed_sql = f.read()
        cursor.executescript(seed_sql)
    print("Mock cloud inventory seeded successfully.")

    conn.commit()
    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    initialize_database()