import requests
import json
BASE = " http://127.0.0.1:5000/"

url = BASE + 'register'
url2 = BASE + 'login'
url3 = BASE + 'certificate/S3976311@student.rmit.edu.au'
url4 = BASE + 'checkcertificate/246311'

data = {    'studentId': 'S3976311',
            'fName': 'Shubham',
            'lName': 'Pai', 
            'email': 'S3976311@student.rmit.edu.au', 
            'password': 'hahalol', 
            'graduationYear': '2024', 
            'certNo': '246311'}

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
    "email": "S3976311@student.rmit.edu.au",
    "password": "hahalol"
}


print("In test " + url4)
#response = requests.post(url2, data=json.dumps(getdata), headers=headers)
#response = requests.get(url2,params=getdata)
response = requests.get(url3)
#response = requests.get(url4)
print(response.json())
