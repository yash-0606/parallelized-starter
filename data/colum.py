import sqlite3
import os
script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, "../data/2023-11-02.db")
def print_column_names(database_path, table_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    if columns:
        column_names = [column[1] for column in columns]
        print("Column Names:")
        for column_name in column_names:
            print(column_name)
    else:
        print(f"No columns found for table: {table_name}")

    conn.close()

# Example usage:
database_path = "your_database.db"
table_name = "your_table_name"
print_column_names(db_path, 'rides')