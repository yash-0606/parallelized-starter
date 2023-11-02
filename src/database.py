import sqlite3
import os

script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, "../data/2023-11-02.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS driver_analyses (driver_id INTEGER PRIMARY KEY NOT NULL, efficiency TEXT NOT NULL, inefficiencyReason TEXT, payout REAL NOT NULL, bonus REAL NOT NULL);
""")


def get_driver_rides(driver_id) -> list[sqlite3.Row]:
    """
    Get driver rides with driver ID. Can convert return value to a dictionary with dict()
    """
    cursor.execute("SELECT * FROM rides WHERE driver_id = ?", (driver_id,))
    rows = cursor.fetchall()
    return rows


def get_driver_details(driver_id) -> sqlite3.Row:
    """
    Get a driver's details by ID. Can convert return value to a dictionary with dict()
    """
    cursor.execute("SELECT * FROM drivers WHERE id = ?", (driver_id,))
    row = cursor.fetchone()
    return row


def get_drivers(limit=250) -> list[sqlite3.Row]:
    """
    Get drivers up to a limit (default: 250). Can be specified as None.
    """
    if limit == None:
        cursor.execute("SELECT * FROM drivers")
    else:
        cursor.execute("SELECT * FROM drivers LIMIT ?", (limit,))
    return cursor.fetchall()


def insert_analysis_row(driver_id: int, efficiency: str, inefficiencyReason: str, payout: float, bonus: float):
    # TODO: Implement a function that inserts a row with your overall analysis details into the table 'driver_analyses' (that includes their efficiency, payout and bonus)
    pass  # <- delete me


conn.close()
