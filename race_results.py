import sqlite3
import json
import sys
import os

def get_race_year_info(race_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('racedata.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM races WHERE race_name = ? ORDER BY date DESC", (race_name,))
    rows = cursor.fetchall()

    # Convert results to JSON
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    conn.close()

    return result

def get_race_attendance_records(race_name,sex):
    # Connect to the SQLite database
    conn = sqlite3.connect('racedata.sqlite')
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT s.participant_name, COUNT(*) AS attendance_count
        FROM races r
        INNER JOIN statistics s ON r.id = s.race_id
        WHERE r.race_name = ? AND s.sex = ?
        GROUP BY participant_name, runner_id
        ORDER BY attendance_count DESC
        LIMIT 10;
        """,
        (race_name,sex,)
    )

    rows = cursor.fetchall()

    # Convert results to JSON
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    conn.close()

    return result

def get_race_time_records(race_name,sex,division):
    # Connect to the SQLite database
    conn = sqlite3.connect('racedata.sqlite')
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT s.participant_name, s.time
        FROM races r
        INNER JOIN statistics s ON r.id = s.race_id
        WHERE r.race_name = ? AND s.sex = ? AND division = ?
        ORDER BY s.time DESC
        LIMIT 10;
        """,
        (race_name,sex,division,)
    )

    rows = cursor.fetchall()

    # Convert results to JSON
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    conn.close()

    return result

def get_race_results(race_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('racedata.sqlite')
    cursor = conn.cursor()

    # Execute a query to fetch data for the given race
    cursor.execute("SELECT * FROM statistics WHERE race_id = ?", (race_id,))
    rows = cursor.fetchall()

    # Convert results to JSON
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    conn.close()
    
    return result

def write_to_file(directory, filename, content):
    """Writes content to a file, creating the directory if it doesn't exist."""

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Construct the full file path
    filepath = os.path.join(directory, filename)

    # Open the file in write mode ('w')
    with open(filepath, 'w') as file:
        print(content, file=file)
        file.close

if __name__ == "__main__":
    # Get the race from command-line arguments
    if len(sys.argv) != 2:
        raise Exception("A race name is required")
    
    race_name = sys.argv[1]
    race_information = get_race_year_info(race_name)
    race_directory = 'docs/'+race_name.lower().replace(' ','-')

    write_to_file(
        race_directory,
        'race.json',
        json.dumps(race_information)
    )

    write_to_file(
        race_directory,
        'attendance_f.json',
        json.dumps(get_race_attendance_records(race_name,'F'))
    )

    write_to_file(
        race_directory,
        'attendance_m.json',
        json.dumps(get_race_attendance_records(race_name,'M'))
    )

    write_to_file(
        race_directory,
        'run_records_f.json',
        json.dumps(get_race_time_records(race_name,'F','Run'))
    )

    write_to_file(
        race_directory,
        'run_records_m.json',
        json.dumps(get_race_time_records(race_name,'M','Run'))
    )

    for race in race_information:
        race_results = get_race_results(race['id'])
        write_to_file(
            race_directory,
            race['date'][:4]+'.json',
            json.dumps(race_results)
        )

    print('OK')
