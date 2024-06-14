from flask import Flask, render_template, request
import csv
import sqlite3

app = Flask(__name__)

# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('form_data.db')
    conn.row_factory = sqlite3.Row  # Access rows by column names
    return conn

# Function to initialize database (create table if not exists)
def init_db():
    with app.app_context():
        conn = get_db_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS FormData (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    college TEXT NOT NULL,
                    pref1 TEXT,
                    pref2 TEXT,
                    pref3 TEXT
                )
            ''')

# Initialize the database
init_db()

# Define route for the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        college = request.form['college']
        pref1 = request.form['pref1']
        pref2 = request.form['pref2']
        pref3 = request.form['pref3']

        # Insert data into SQLite database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO FormData (name, college, pref1, pref2, pref3)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, college, pref1, pref2, pref3))
        
        # Export data to CSV file
        export_to_csv()

    # Fetch college names from a predefined list or another table in real scenario
    colleges = [
        'AVV Coimbatore',
        'Bharti Vidyapeeth',
        'Datta Meghe College of Engineering',
        'ICT Jalna',
        'ICT Mumbai',
        'IIT Kanpur',
        'NIT Jalandhar',
        'SS Jondhale College',
        'TSEC Mumbai',
        'VJTI (Chemical)',
        'VJTI (Mechanical)'
    ]

    # Project preferences 
    projects = ['Project1', 'Project2', 'Project3']

    return render_template('form.html', colleges=colleges, projects=projects)

# Function to export data to CSV file
def export_to_csv():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM FormData')
        rows = cursor.fetchall()
        with open('form_data.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([i[0] for i in cursor.description])  # Write headers
            csv_writer.writerows(rows)

if __name__ == '__main__':
    app.run(debug=True)
