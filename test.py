import requests
import json
BASE = " http://127.0.0.1:5000/"

url = BASE + 'register'
url2 = BASE + 'login'
url3 = BASE + 'certificate/S3976313@student.rmit.edu.au'
url4 = BASE + 'checkcertificate/2476312'

data = {    'studentId': 'S3976313',
            'fName': 'Deven',
            'lName': 'Pai', 
            'email': 'S3976313@student.rmit.edu.au', 
            'password': 'Deven@123', 
            'graduationYear': '2024',
            'number' : '+61434309705'
        }

testdata = {"fName":"Thuc Hi","lName":"Tran","email":"thuchitran@gmail.com","password":"Ab!","studentId":"s3996832","graduationYear":"2024","certNo":"241216"}

headers = {'Content-type': 'application/json'}


getdata = {
    "email": "S3976313@student.rmit.edu.au",
    "password": "Deven@12"
#    "password": "1111"
}


#response = requests.post(url, data=json.dumps(data), headers=headers)
#response = requests.post(url2, data=json.dumps(getdata), headers=headers)
#response = requests.get(url3)
response = requests.get(url4)
print(response.json())
