import sqlite3
import json
import sys

def query_database(year, race_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('race_results.db')
    cursor = conn.cursor()

    # Execute a query to fetch data for the given year
    cursor.execute("SELECT * FROM results WHERE year = ? AND race_name = ?", (year,race_name,))
    rows = cursor.fetchall()

    # Convert results to JSON
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    conn.close()

    # Output JSON data
    print(json.dumps(result))

if __name__ == "__main__":
    # Get the year from command-line arguments
    if len(sys.argv) > 1:
        year = sys.argv[1]
    else:
        year = '2023'  # Default year
    if len(sys.argv) > 2:
        race_name = sys.argv[2]
    else:
        race_name = 'Heart of the Hills Run' # Default Race
    query_database(year, sys.argv[2])