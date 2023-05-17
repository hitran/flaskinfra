from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for,jsonify)
import mysql.connector
import bcrypt
import os

app = Flask(__name__)

# establish database connection
mydb = mysql.connector.connect(
  host="db4free.net",
  port=3306,
  user="infrafinal",
  password="infrafinal2505",
  database="studentinfra"
)

# create cursor
mycursor = mydb.cursor()


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


# Define the routes for CRUD operations

# Register a new student
@app.route('/register', methods=['POST'])
def register_student():
    try:
        studentId = request.json['studentId']
        fName = request.json['fName']
        lName = request.json['lName']
        email = request.json['email']
        password = request.json['password']
        password_bytes_value = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes_value, salt)
        graduationYear = request.json['graduationYear']
        certNo = request.json['certNo']
        statement = 'INSERT INTO student (studentId, fname, lname, graduationYear, email, password, certNo) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        values = (studentId, fName, lName, graduationYear, email, hashed_password, certNo)
        mycursor.execute(statement, values)
        mydb.commit()
        return jsonify({'message': 'Student record saved successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Student record not saved','exception':  str(e)     }), 500

# Log student in
@app.route('/login', methods=['POST'])
def get_student():
    print("Student email ID is  : " + request.json['email'])
    print("Password is " + request.json['password'])
    mycursor.execute("SELECT password FROM student WHERE email = %s", (request.json['email'],))
    student_hashed_password = mycursor.fetchone()
    print(student_hashed_password)
    if bcrypt.checkpw(request.json['password'].encode('utf-8'), student_hashed_password[0].encode()): 
        return jsonify({'Email Id': request.json['email'], 'status':'success'}), 200
    else:
        return jsonify({'Email Id': request.json['email'], 'status':'failed'}), 404

# Fetch certificate details
@app.route('/certificate/<email_id>', methods=['GET'])
def get_certificate(email_id):
    print("Student email ID is  : " + email_id )
    mycursor.execute("SELECT * FROM certificate JOIN student on certificate.certNo = student.certNo WHERE student.email = %s", (email_id,))
    certificate = mycursor.fetchone()
    print(certificate)
    if certificate:
        return jsonify({'certNo': certificate[0], 'document': str(certificate[1])})
    else:
        return jsonify({'message': 'certificate not found'}), 404

# check certificate details
@app.route('/checkcertificate/<certificate_id>', methods=['GET'])
def check_certificate(certificate_id):
    print("Certificate ID is  : " + certificate_id)
    mycursor.execute("SELECT student.studentId, student.fname, student.lname FROM certificate JOIN student on certificate.certNo = student.certNo WHERE certificate.certNo = %s", (certificate_id,))
    student = mycursor.fetchone()
    print(student)
    if student:
        return jsonify({'studentId': student[0], 'fname': student[1], 'lname':student[2] })
    else:
        return jsonify({'message': 'certificate not found'}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)