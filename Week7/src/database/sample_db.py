import sqlite3
import os

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

db_path = "database/sample.db"

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Recreate table
cursor.execute("DROP TABLE IF EXISTS sales")

cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT,
    genre TEXT,
    revenue REAL,
    year INTEGER,
    country TEXT
)
""")

# More realistic artist data
records = [
    ("Arijit Singh", "Pop", 110.0, 2023, "India"),
    ("Taylor Swift", "Pop", 55.0, 2023, "USA"),
    ("Drake", "Hip-Hop", 125.0, 2023, "Canada"),
    ("Norah Jones", "Jazz", 78.0, 2023, "USA"),
    ("Badshah", "Hip-Hop", 98.0, 2023, "India"),

    ("Arijit Singh", "Pop", 72.0, 2022, "India"),
    ("Taylor Swift", "Pop", 68.0, 2022, "USA"),
    ("Drake", "Hip-Hop", 115.0, 2022, "Canada"),
    ("Norah Jones", "Jazz", 62.0, 2022, "USA"),
    ("Badshah", "Hip-Hop", 88.0, 2022, "India"),

    ("Arijit Singh", "Pop", 135.0, 2024, "India"),
    ("Taylor Swift", "Pop", 80.0, 2024, "USA"),
    ("Drake", "Hip-Hop", 145.0, 2024, "Canada"),
    ("Norah Jones", "Jazz", 92.0, 2024, "USA"),
    ("Badshah", "Hip-Hop", 108.0, 2024, "India"),

    ("Ludwig van Beethoven", "Classical", 65.0, 2023, "Germany"),
    ("Calvin Harris", "EDM", 155.0, 2023, "UK"),
    ("Shreya Ghoshal", "Pop", 210.0, 2023, "India"),
    ("Imagine Dragons", "Rock", 175.0, 2023, "USA"),
    ("Kendrick Lamar", "Hip-Hop", 195.0, 2023, "USA")
]

# Insert data
cursor.executemany("""
INSERT INTO sales (artist, genre, revenue, year, country)
VALUES (?, ?, ?, ?, ?)
""", records)

# Commit and close
conn.commit()
conn.close()

print("Database setup completed with realistic artist data.")