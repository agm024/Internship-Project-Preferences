from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('form_data.db')
    conn.row_factory = sqlite3.Row  # Access rows by column names
    return conn

# Initialize the database
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
            conn.commit()

# Initialize the database on application start
init_db()

# Route for submitting the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form['name']
            college = request.form['college']
            pref1 = request.form['pref1']
            pref2 = request.form['pref2']
            pref3 = request.form['pref3']

            # Perform basic validation
            if not (name and college):
                flash("Name and College fields are required.", 'error')
                return redirect(url_for('index'))

            # Insert data into SQLite database
            conn = get_db_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO FormData (name, college, pref1, pref2, pref3)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, college, pref1, pref2, pref3))
                conn.commit()

            # Export data to CSV file
            export_to_csv()

            # Flash success message
            flash('Form submitted successfully!', 'success')

            # Redirect to success page
            return redirect(url_for('success'))  # Ensure this line redirects correctly

        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('index'))

    # Fetch colleges and projects from a predefined list (you can modify this)
    colleges = [
        'AVV Coimbatore', 'Bharti Vidyapeeth', 'Datta Meghe COE', 
        'ICT Jalna', 'ICT Mumbai', 'IIT Kanpur', 'NIT Jalandhar', 
        'SS Jondhale COE', 'TSEC Mumbai', 'VJTI (Chemical)', 'VJTI (Mechanical)'
    ]

    projects = [
        'Synergistic wetting agents for dishwash bar', 'Powdered surfactant for Home care application', 
        'Generative Design and Topology Optimization', 'Hybrid modelling for fire simulation and fire retardant material design',
        'Bonding 3D Printed polymer parts', 'Advancements in Non-destructive testing for Building Science',
        '3D Printing of large structures - Buildings & Structures', 'Coconut oil sensory improvement',
        'Feasibility study of EOR Surfactant production in India',
        'Improve Dirt Pickup Resistance of Water based Traffic Paint',
        'LD/LLDPE PCR competitive landscape technology, Supply & Demand',
        'HDPE blow moulded PCR technology challenges & Opportunities',
        'AR technology, players & capacity'
    ]

    return render_template('form.html', colleges=colleges, projects=projects)


# Route for the success page
@app.route('/success')
def success():
    return render_template('success.html')

# Function to export data to CSV file
def export_to_csv():
    conn = get_db_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM FormData')
        rows = cursor.fetchall()
        with open('form_data.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([i[0] for i in cursor.description])  # Write headers
            csv_writer.writerows(rows)

if __name__ == '__main__':
    app.run(debug=True)
