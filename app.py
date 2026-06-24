'''from flask import Flask, request,jsonify
import psycopg2

app =Flask(__name__)

#database config
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "0598"

def get_db_connection():
    return psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user =DB_USER,
        password =DB_PASSWORD
    )

#CREATE STUDENT_TABLE
def create_student_table():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
             CREATE TABLE IF NOT EXISTS student_table(
                 student_id SERIAL PRIMARY KEY,
                 student_name TEXT NOT NULL,
                 roll_number TEXT NOT NULL UNIQUE,
                 email TEXT NOT  NULL UNIQUE
                );
""")
    connection.commit()
    cur.close()
    connection.close()

create_student_table()


@app.route("/send_data", methods = ['POST'])
def send_data():
    student_name = request.json['student_name']
    roll_number = request.json['roll_number']
    email = request.json['email']
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
        INSERT  INTO student_table(student_name ,roll_number, email) VALUES(%s,%s,%s)
""",(student_name,roll_number,email))
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message":"Data sended successfully"}),201
    

@app.route("/get_data", methods =['GET'])
def get_data():
    connection =get_db_connection()
    cur =connection.cursor()
    cur.execute("""
          select * from student_table
""")
    Data = cur.fetchone()
    cur.close()
    connection.close()
    return jsonify({
        "student_id":Data[0],
        "student-name":Data[1],
        "roll_number ":Data[2],
        "email":Data[3]

    }),200
    
    
@app.route("/update_data",methods=['put'])
def update_data():
    student_id= request.json['student_id']
    student_name = request.json['student_name']
    roll_number = request.json['roll_number']
    email = request.json['email']
    connection=get_db_connection()
    cur =connection.cursor()
    cur.execute("""
          UPDATE student_table
          SET student_name =%s,
              roll_number=%s,
              email=%s
          WHERE student_id=%s 
""",(student_name, roll_number, email, student_id))
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message":"Data updated successfully"}),200


@app.route("/delete_data",methods=['DELETE'])
def delete_data():
    student_id= int(request.json['student_id'])
    connection=get_db_connection()
    cur =connection.cursor()
    cur.execute("""
          DELETE from student_table
          WHERE student_id=%s 
""",(student_id,))
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message":"Data deleted successfully"}),200


if __name__ == "__main__":
    app.run(debug=True)'''
    
    
from flask import Flask, request,jsonify
import psycopg2
from flask_bcrypt import Bcrypt

app =Flask(__name__)

bcrypt = Bcrypt(app)

#database config
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "0598"

def get_db_connection():
    return psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user =DB_USER,
        password =DB_PASSWORD
    )

#CREATE STUDENT_TABLE
def create_student_table():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
             CREATE TABLE IF NOT EXISTS users_table(
                 user_id SERIAL PRIMARY KEY,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL,
                 email TEXT NOT  NULL UNIQUE
                );
""")
    connection.commit()
    cur.close()
    connection.close()

create_student_table()

@app.route('/signup', methods = ['POST'])
def signup():

    username =request.json["username"]
    email =request.json["email"]
    password =request.json["password"]
    
    hashed_username= bcrypt.generate_password_hash(username).decode("utf-8")
    '''hashed_password= bcrypt.generate_password_hash(password).decode('utf-8')
    hashed_email= bcrypt.generate_password_hash(email).decode('utf-8')'''

    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
         INSERT INTO users_table(username,email,password) VALUES(%s,%s,%s)
""",(hashed_username,email,password))#use hashed_username,hashed_password,hashed_email
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message":"signup successful"})

if __name__ == "__main__":
    app.run(debug=True)