import sqlite3
import os
#makes demo sqlite db(creates table and puts dummy data in it)
#SQLite is lightweight(minimal resource requirements, extremely small, typically less than 1MB,entire database stored in a single cross-platform disk file.), serverless(does not follow a client-server model, because of its unique architecture that integrates the database engine directly into the application rather than running it as a separate background servic), and easy to integrate(SQLite is compatible with almost all major programming languages, A database file created on one system (e.g., Windows) can be copied and used on another ).
#sqlite is ideal for small-scale applications and local development.

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

db_path = "database/sample.db"

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Recreate table: fresh start
cursor.execute("DROP TABLE IF EXISTS sales") 

#table structure
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

records = [

    # 2022
    ("Arijit Singh", "Pop", 72.0, 2022, "India"),
    ("Taylor Swift", "Pop", 68.0, 2022, "USA"),
    ("Drake", "Hip-Hop", 115.0, 2022, "Canada"),
    ("Norah Jones", "Jazz", 62.0, 2022, "USA"),
    ("Badshah", "Hip-Hop", 88.0, 2022, "India"),
    ("Shreya Ghoshal", "Pop", 95.0, 2022, "India"),
    ("Imagine Dragons", "Rock", 120.0, 2022, "USA"),
    ("Kendrick Lamar", "Hip-Hop", 140.0, 2022, "USA"),
    ("Calvin Harris", "EDM", 130.0, 2022, "UK"),
    ("Adele", "Pop", 150.0, 2022, "UK"),
    ("Ed Sheeran", "Pop", 145.0, 2022, "UK"),
    ("BTS", "K-Pop", 180.0, 2022, "South Korea"),
    ("The Weeknd", "R&B", 160.0, 2022, "Canada"),
    ("Coldplay", "Rock", 135.0, 2022, "UK"),
    ("Eminem", "Hip-Hop", 170.0, 2022, "USA"),

    # 2023
    ("Arijit Singh", "Pop", 110.0, 2023, "India"),
    ("Taylor Swift", "Pop", 55.0, 2023, "USA"),
    ("Drake", "Hip-Hop", 125.0, 2023, "Canada"),
    ("Norah Jones", "Jazz", 78.0, 2023, "USA"),
    ("Badshah", "Hip-Hop", 98.0, 2023, "India"),
    ("Shreya Ghoshal", "Pop", 210.0, 2023, "India"),
    ("Imagine Dragons", "Rock", 175.0, 2023, "USA"),
    ("Kendrick Lamar", "Hip-Hop", 195.0, 2023, "USA"),
    ("Calvin Harris", "EDM", 155.0, 2023, "UK"),
    ("Ludwig van Beethoven", "Classical", 65.0, 2023, "Germany"),
    ("Adele", "Pop", 185.0, 2023, "UK"),
    ("Ed Sheeran", "Pop", 175.0, 2023, "UK"),
    ("BTS", "K-Pop", 220.0, 2023, "South Korea"),
    ("The Weeknd", "R&B", 200.0, 2023, "Canada"),
    ("Coldplay", "Rock", 165.0, 2023, "UK"),
    ("Eminem", "Hip-Hop", 210.0, 2023, "USA"),

    # 2024
    ("Arijit Singh", "Pop", 135.0, 2024, "India"),
    ("Taylor Swift", "Pop", 80.0, 2024, "USA"),
    ("Drake", "Hip-Hop", 145.0, 2024, "Canada"),
    ("Norah Jones", "Jazz", 92.0, 2024, "USA"),
    ("Badshah", "Hip-Hop", 108.0, 2024, "India"),
    ("Shreya Ghoshal", "Pop", 240.0, 2024, "India"),
    ("Imagine Dragons", "Rock", 200.0, 2024, "USA"),
    ("Kendrick Lamar", "Hip-Hop", 220.0, 2024, "USA"),
    ("Calvin Harris", "EDM", 190.0, 2024, "UK"),
    ("Adele", "Pop", 210.0, 2024, "UK"),
    ("Ed Sheeran", "Pop", 205.0, 2024, "UK"),
    ("BTS", "K-Pop", 260.0, 2024, "South Korea"),
    ("The Weeknd", "R&B", 230.0, 2024, "Canada"),
    ("Coldplay", "Rock", 195.0, 2024, "UK"),
    ("Eminem", "Hip-Hop", 250.0, 2024, "USA"),
]

# insert in bulk 
cursor.executemany("""
INSERT INTO sales (artist, genre, revenue, year, country)
VALUES (?, ?, ?, ?, ?)
""", records)

# Commit and close
conn.commit()
conn.close()

print(f"Database setup completed with {len(records)} records.")