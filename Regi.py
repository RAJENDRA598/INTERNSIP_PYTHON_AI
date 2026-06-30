from flask import Flask, request, jsonify
import psycopg2
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "0598"


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def create_data_table():
    connection = get_db_connection()
    cur = connection.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS data_table(
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone_number VARCHAR(15) NOT NULL,
            college VARCHAR(100) NOT NULL
        );
    """)
    connection.commit()
    cur.close()
    connection.close()
    
create_data_table()
@app.route('/Registration', methods=['POST'])
def Registration():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone_number = data.get("phone_number")
    college = data.get("college")

    if not username or not email or not password or not phone_number or not college:
        return jsonify({"error": "All fields are required"}), 400
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
        SELECT * FROM data_table
        WHERE username=%s OR email=%s
    """, (username, email))
    existing_user = cur.fetchone()
    if existing_user:
        cur.close()
        connection.close()
        return jsonify({
            "error": "Username or Email already exists"
        }), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cur.execute("""
        INSERT INTO data_table
        (username, email, password, phone_number, college)
        VALUES (%s, %s, %s, %s, %s)
    """, (username,email,hashed_password,phone_number,college ))
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({
        "message": "User Registered Successfully"
    }), 201

from flask import request, jsonify

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validate required fields
    if not username or not email or not password:
        return jsonify({
            "error": "Username, Email and Password are required"
        }), 400

    connection = get_db_connection()
    cur = connection.cursor()

    # Check if username and email belong to the same user
    cur.execute("""
        SELECT user_id, username, email, password
        FROM data_table
        WHERE username = %s AND email = %s
    """, (username, email))

    user = cur.fetchone()

    if user is None:
        cur.close()
        connection.close()
        return jsonify({
            "error": "Invalid Username or Email"
        }), 404

    user_id = user[0]
    db_username = user[1]
    db_email = user[2]
    hashed_password = user[3]

    # Verify password
    if not bcrypt.check_password_hash(hashed_password, password):
        cur.close()
        connection.close()
        return jsonify({
            "error": "Invalid Password"
        }), 401

    cur.close()
    connection.close()

    # Login successful
    return jsonify({
        "message": "Login Successful",
        "user_id": user_id,
        "username": db_username,
        "email": db_email
    }), 200
if __name__ == "__main__":
    app.run(debug=True)