# setup_db.py
import sqlite3

DB_FILE = "agent_data.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the table for structured data (e.g., finance/employee facts)
cursor.execute("""
CREATE TABLE IF NOT EXISTS company_records (
    id INTEGER PRIMARY KEY,
    metric TEXT,
    value REAL,
    unit TEXT,
    quarter TEXT
);
""")

# Insert sample factual data
data = [
    ('Revenue', 150.5, 'Million USD', 'Q1'),
    ('Profit', 45.2, 'Million USD', 'Q1'),
    ('Revenue', 165.1, 'Million USD', 'Q2'),
    ('Profit', 51.9, 'Million USD', 'Q2'),
    ('Total Employees', 1200, 'People', 'Q2'),
]
cursor.executemany("INSERT INTO company_records (metric, value, unit, quarter) VALUES (?, ?, ?, ?)", data)

conn.commit()
conn.close()
print(f"Database {DB_FILE} created and populated.")