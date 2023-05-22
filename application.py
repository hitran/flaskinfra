from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for,jsonify,session)
from flask_session import Session
import mysql.connector
import bcrypt
import os
import re

class StringLengthError(Exception):
    pass

app = Flask(__name__)
app.secret_key = 'infrafinal'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

# Define the routes for CRUD operations

# Register a new student
@app.route('/register', methods=['POST'])
def register_student():
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
    try:
        mydb.start_transaction()
        studentId = request.json['studentId']
        fName = request.json['fName']
        lName = request.json['lName']
        email = request.json['email']
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ConstraintError("Incorrect email format")
        password = request.json['password']
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[\W_]).+$'
        if len(password) < 8 and not re.match(pattern, password):
            raise ConstraintError("Incorrect password format")
        password_bytes_value = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes_value, salt)
        graduationYear = request.json['graduationYear']
        number = request.json['number']
        if len(number) != 12:
             raise StringLengthError("Incorrect phone number")
        certNo = str(graduationYear[-2:]) + str(studentId[-5:]) 
        role = "user"
        statement = 'INSERT INTO student (studentId, fname, lname, graduationYear, email, password, certNo, role, number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values = (studentId, fName, lName, graduationYear, email, hashed_password, certNo, role, number)
        mycursor.execute(statement, values)
        print("Student data inserted")
        statement2 = 'INSERT INTO certificate (certNo, document) VALUES (%s,%s)'
        values2 = (certNo,'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')
        mycursor.execute(statement2, values2)
        print("Certificate details generated")
        mydb.commit()
        return jsonify({'message': 'Student record saved successfully','status':'success'}), 201
    except Exception as e:
        return jsonify({'message': 'Student record not saved','exception':  str(e),'status':'failed'}), 500
    finally:
        mycursor.close()
        mydb.close()

# Log student in
@app.route('/login', methods=['POST'])
def login():
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
    try:
        print("Student email ID is  : " + request.json['email'])
        print("Password is " + request.json['password'])
        mycursor.execute("SELECT password, role FROM student WHERE email = %s", (request.json['email'],))
        student = mycursor.fetchall()
        if student:
            print(student)
            if bcrypt.checkpw(request.json['password'].encode('utf-8'), student[0][0].encode()): 
                session['logged_in'] = True
                session['username'] = request.json['email']
                return jsonify({'Email Id': request.json['email'], 'status':'success', 'role' : str(student[0][1]) }), 200
            else:
                return jsonify({'Email Id': request.json['email'], 'status':'failed', 'reason': 'incorrect email/password'}), 404
        else:
            return jsonify({'Email Id': request.json['email'], 'status':'failed', 'reason': 'incorrect email/password'}), 404
    except Exception as e:
        return jsonify({'message': 'Student record not found','exception':  str(e),'status':'failed'}), 500
    finally:
        mycursor.close()
        mydb.close()

# Fetch certificate details
@app.route('/certificate/<email_id>', methods=['GET'])
def get_certificate(email_id):
    
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
    try:   
        print("Student email ID is  : " + email_id ) 
        if not (session.get('username') == email_id):
            return jsonify({'message': 'Invalid user data access','exception':  'No rights to view','status' : 'failed'}), 404
        mycursor.execute("SELECT student.studentId, student.fname, student.lname, certificate.certNo,certificate.document FROM certificate JOIN student on certificate.certNo = student.certNo WHERE student.email = %s", (email_id,))
        certificate = mycursor.fetchall()
        if certificate:
            print(certificate)
            certificate =certificate[0]
            return jsonify({'studentId': certificate[0], 'fname': certificate[1], 'lname':certificate[2], 'certNo':certificate[3], 'document': str(certificate[4]),'status':'success'}), 200
        else:
            return jsonify({'message': 'certificate not found','status':'failed'}), 404
    except Exception as e:
        return jsonify({'message': 'Student record not saved','exception':  str(e),'status':'failed'}), 500
    finally:
        mycursor.close()
        mydb.close()

# check certificate details
@app.route('/checkcertificate/<certificate_id>', methods=['GET'])
def check_certificate(certificate_id):
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
    try:    
        print("Certificate ID is  : " + certificate_id)
        mycursor.execute("SELECT student.studentId, student.fname, student.lname, certificate.certNo FROM student JOIN certificate on certificate.certNo = student.certNo WHERE certificate.certNo = %s", (certificate_id,))
        student = mycursor.fetchall()
        print(student)
        if student:
            student =student[0]
            print(student)
            return jsonify({'studentId': student[0], 'fname': student[1], 'lname':student[2], 'certNo':student[3], 'status' : 'success' }),200
        else:
            return jsonify({'message': 'certificate not found', 'status' : 'failed'}), 404
    except Exception as e:
        return jsonify({'message': 'certificate not found','exception':  str(e), 'status' : 'failed'}), 500
    finally:
        mycursor.close()
        mydb.close()

# Update person details 
@app.route('/updateperson/<email_id>', methods=['PUT'])
def update_person(email_id):
    # establish database connection
    if not (session['username'] == 'root@root.com'):
        return jsonify({'message': 'Student record not updated','exception':  'No rights to update','status' : 'failed'})
    mydb = mysql.connector.connect(
    host="db4free.net",
    port=3306,
    user="infrafinal",
    password="infrafinal2505",
    database="studentinfra"
    )
    # create cursor
    mycursor = mydb.cursor()
    try:
        mydb.start_transaction()
        studentId = request.json['studentId']
        fName = request.json['fName']
        lName = request.json['lName']
        graduationYear = request.json['graduationYear']
        number = request.json['number']
        if len(number) != 12:
             raise StringLengthError("Incorrect phone number")
        role = request.json['role']
        statement = 'UPDATE student SET studentId = %s, fname = %s, lname = %s, graduationYear = %s, role = %s, number = %s WHERE email = %s'
        values = (studentId, fName, lName, graduationYear, role, number)
        mycursor.execute(statement, values)
        print("Student data Updated")
        mydb.commit()
        return jsonify({'message': 'Student record updated successfully','status' : 'success'}), 201
    except Exception as e:
        return jsonify({'message': 'Student record not updated','exception':  str(e),'status' : 'failed'}), 500
    finally:
        mycursor.close()
        mydb.close()

#log currently logged in person out
@app.route('/logout', methods=['PUT'])
def logout():
    # Clear the user's session data
    session.clear()
    return jsonify({'status':'success'})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)