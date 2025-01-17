from flask import render_template, Flask, request, jsonify, session
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'



def initialize_database():
    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            profile_picture_url TEXT DEFAULT 'default-profile.jpg',
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS flood_reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            status TEXT DEFAULT 'Unverified',
            description TEXT NOT NULL,
            image_url TEXT,
            video_url TEXT,
            location TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verified_at TIMESTAMP,
            verified_by INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (verified_by) REFERENCES users(user_id) ON DELETE SET NULL
        );
        """)

        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        connection.close()

@app.route('/map/second')
def second_map():
    return render_template('map_nongov.html')

@app.route('/')
def home():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.json

    real_name = data.get('realName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([real_name, last_name, username, email, password]):
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    email_pattern = r'^(krasi4367@gmail\.com|[a-zA-Z0-9._%+-]+@([a-zA-Z0-9-]+\.)?(gov|mil|gouv|gov\.[a-z]{2}|govt|canada\.ca))$'
    is_government_user = 1 if re.match(email_pattern, email) else 0

    full_name = f"{real_name} {last_name}"

    try:
        connection = sqlite3.connect("flood_monitor.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO users (name, email, username, password, is_government_user)
        VALUES (?, ?, ?, ?, ?)
        """, (full_name, email, username, password, is_government_user))
        connection.commit()

        return jsonify({"status": "success", "message": "User registered successfully."}), 201
    except sqlite3.Error as e:
        print(f"Error during registration: {e}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        data = request.json
        email_or_username = data.get('emailOrUsername')
        password = data.get('password')

        if not email_or_username or not password:
            return jsonify({"status": "error", "message": "Both username/email and password are required."}), 400

        connection = sqlite3.connect("flood_monitor.db")
        cursor = connection.cursor()

        try:
            query = """
                SELECT password FROM users 
                WHERE email = ? OR username = ?
            """
            cursor.execute(query, (email_or_username, email_or_username))
            result = cursor.fetchone()

            if result:
                stored_password = result[0]

                if stored_password == password:
                    session['user'] = email_or_username
                    return jsonify({"status": "success", "message": "Login successful!", "redirect": "/map"}), 200
                else:
                    return jsonify({"status": "error", "message": "Invalid password."}), 401
            else:
                return jsonify({"status": "error", "message": "User not found."}), 404
        except Exception as e:
            print(f"Error during login: {e}")
            return jsonify({"status": "error", "message": "Internal server error."}), 500
        finally:
            cursor.close()
            connection.close()


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"status": "success", "message": "Logged out successfully!", "redirect": "/login"}), 200


@app.route('/map')
def map():
    if 'user' not in session:
        return "Unauthorized Access", 401

    email_or_username = session['user']
    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT is_government_user FROM users WHERE email = ? OR username = ?", (email_or_username, email_or_username))
        result = cursor.fetchone()

        if result and result[0] == 1:
            return render_template('map.html')
        else:
            return render_template('map_nongov.html')
    finally:
        cursor.close()
        connection.close()




@app.route('/report', methods=['POST'])
def report():
    data = request.json
    address = data.get('address')
    description = data.get('description')
    lat = data.get('lat')
    lon = data.get('lon')

    if not all([address, description, lat, lon]):
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    try:
        connection = sqlite3.connect("flood_monitor.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO flood_reports (location, description, latitude, longitude)
        VALUES (?, ?, ?, ?)
        """, (address, description, lat, lon))
        connection.commit()

        return jsonify({"status": "success", "message": "Report saved successfully."}), 201
    except sqlite3.Error as e:
        print(f"Error saving report: {e}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized Access", 401

    email_or_username = session['user']
    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT name, email, username, profile_picture_url
            FROM users
            WHERE email = ? OR username = ?
        """, (email_or_username, email_or_username))
        user = cursor.fetchone()

        if user:
            user_data = {
                'name': user[0],
                'email': user[1],
                'username': user[2],
                'profile_picture_url': user[3],
            }
            return render_template('profile.html', user=user_data)
        else:
            return "User not found", 404
    finally:
        cursor.close()
        connection.close()
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Unauthorized access"}), 401

    data = request.json
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')

    if not all([name, email, username]):
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    email_or_username = session['user']
    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET name = ?, email = ?, username = ?, updated_at = CURRENT_TIMESTAMP
            WHERE email = ? OR username = ?
        """, (name, email, username, email_or_username, email_or_username))
        connection.commit()

        session['user'] = email
        return jsonify({"status": "success", "message": "Profile updated successfully"})
    except sqlite3.Error as e:
        print(f"Error updating profile: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    finally:
        cursor.close()
        connection.close()
@app.route('/get_user_profile', methods=['GET'])
def get_user_profile():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Unauthorized access"}), 401

    email_or_username = session['user']
    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT name, email, username, profile_picture_url
            FROM users
            WHERE email = ? OR username = ?
        """, (email_or_username, email_or_username))
        user = cursor.fetchone()

        if user:
            return jsonify({
                "status": "success",
                "name": user[0],
                "email": user[1],
                "username": user[2],
                "profile_picture_url": user[3],
            })
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404
    except sqlite3.Error as e:
        print(f"Error fetching user profile: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_reports', methods=['GET'])
def get_reports():
    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT report_id, description, location, latitude, longitude, status FROM flood_reports")
        reports = cursor.fetchall()

        return jsonify([
            {
                "report_id": r[0],
                "description": r[1],
                "location": r[2],
                "latitude": r[3],
                "longitude": r[4],
                "status": r[5] if r[5] else 'Unverified'
            }
            for r in reports
        ])
    except Exception as e:
        print(f"Error fetching reports: {e}")
        return jsonify([])
    finally:
        cursor.close()
        connection.close()



@app.route('/update_report_status', methods=['POST'])
def update_report_status():
    data = request.json
    report_id = data.get('report_id')
    status = data.get('status')

    if not report_id or not status:
        return jsonify({"success": False, "message": "Invalid data."}), 400

    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE flood_reports SET status = ? WHERE report_id = ?", (status, report_id))
        connection.commit()

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error updating report status: {e}")
        return jsonify({"success": False, "message": "Database error."}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/tasks', methods=['GET'])
def tasks():
    return render_template('tasks.html')

@app.route('/clear_reports', methods=['POST'])
def clear_reports():
    data = request.json
    report_ids = data.get('report_ids', [])

    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        for report_id in report_ids:
            cursor.execute("DELETE FROM flood_reports WHERE report_id = ?", (report_id,))
        connection.commit()

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error clearing reports: {e}")
        return jsonify({"success": False}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_reports', methods=['POST'])
def delete_reports():
    data = request.json
    report_ids = data.get('report_ids', [])

    connection = sqlite3.connect("flood_monitor.db")
    cursor = connection.cursor()

    try:
        for report_id in report_ids:
            cursor.execute("DELETE FROM flood_reports WHERE report_id = ?", (report_id,))
        connection.commit()

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error deleting reports: {e}")
        return jsonify({"success": False}), 500
    finally:
        cursor.close()
        connection.close()



if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
