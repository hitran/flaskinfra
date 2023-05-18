import requests
import json
BASE = " http://127.0.0.1:5000/"

url = BASE + 'register'
url2 = BASE + 'login'
url3 = BASE + 'certificate/S3976312@student.rmit.edu.au'
url4 = BASE + 'checkcertificate/246311'

data = {    'studentId': 'S3976312',
            'fName': 'Tanvi',
            'lName': 'Pai', 
            'email': 'S3976312@student.rmit.edu.au', 
            'password': 'tanvi@123', 
            'graduationYear': '2024', 
            'certNo': '246312'}

testdata = {
            "fName":"Hi",
            "lName":"Tran",
            "email":"s3996832@rmit.edu.au",
            "password":"123456",
            "studentId":"S3996832",
            "graduationYear":"2016",
            "certNo":"123456789"
            }
headers = {'Content-type': 'application/json'}


getdata = {
    "email": "S3976312@student.rmit.edu.au",
    "password": "tanvi@123"
#    "password": "1111"
}


print("In test " + url3)
#response = requests.post(url, data=json.dumps(data), headers=headers)
#response = requests.post(url2, data=json.dumps(getdata), headers=headers)
#response = requests.get(url3)
response = requests.get(url4)
print(response.json())
