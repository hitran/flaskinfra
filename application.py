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
# app.config['SESSION_COOKIE_SECURE'] = True
# app.config['SESSION_COOKIE_SAMESITE'] = 'None'

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
        values2 = (certNo,'JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9UaXRsZSAoU3R1ZGVudENlcnRpZmljYXRlKQovUHJvZHVjZXIgKFNraWEvUERGIG0xMTUgR29vZ2xlIERvY3MgUmVuZGVyZXIpPj4KZW5kb2JqCjMgMCBvYmoKPDwvY2EgMQovQk0gL05vcm1hbD4+CmVuZG9iago1IDAgb2JqCjw8L0ZpbHRlciAvRmxhdGVEZWNvZGUKL0xlbmd0aCA0NzE+PiBzdHJlYW0KeJztVdtu1DAQffdX+Ac6nZs9YwkhUdT2GZQ/AFqpEg+U/5eYJGyDUJ0YwiOb1a7lE09mzpwzoYxxXVH8WOP86Wv6lsDKsnv5j03K8/XxPq+L58d0fS/58XuacaeaCUvNz1/SQ/rwWwTj+RsxcNmKGOtii3Ezpes7zeJQ54/n6SHRJS/mCuiomgm4ajOuLU9ztCspgCgNa54+5zextLd5ekosUInNPAKsAN+sgEGjKnH/C/B+AQjBpDXV8oJIXZDbaT87YQU3djnO7vyzjIGk0gATrJeIr3SDIgXRxip/3xXC2C5ujQbaspbHBcxFyTb2tQMILoAwMGIrWyNFeqHuVoBAm1vVDfAhbtkqsDDxALe1JybvlVMuJ5jMgnY8FGxXK9z+/Eg34Z/8cwBSeSAt35OVBrPN1esJWXmDJhq7w2afk1emX9zEYx0vUV6pQwLuynF9lCBgdYzzx5Tfjlndw6KR3bDTXxEd7fXKDVDNzkyAmEaRpg04pkvTZozhuczvepT3xysd6L83TQ67VA28hPROMNDNbc9qggwhRD3htDA3aVFpA8n3utT1xU4vbIhZYgcpRcwGHNBTRF9d3b5br1L/9yN0X1qFospS/r+PRt9HPwBm8zh6CmVuZHN0cmVhbQplbmRvYmoKNyAwIG9iago8PC9GaWx0ZXIgL0ZsYXRlRGVjb2RlCi9MZW5ndGggMzQwPj4gc3RyZWFtCnicpVNBTsQwDLznFfnABttxbEdCHEDsnkH9AbBISBxY/i/htqwWrTAt0FRtlKkn8cwUM/jYoD+0U354TW+paJtWj29fxDyO+12eJ4fndLGr+fk9jbihZIQm+fCU9unujEFpvJ0DpiXnmCcnjushXWw5VysyXpaHfcLjuRC4KJGxZiwk3JWk52Gk29RWAGoHycNjvvSpXOXhJVErapVRnWEGiAOgwgRUKgTQm52AGlFtZwALd1PhE2ATcDv83A+p79UF17Sj81a1CJLql8O1GdDSUap/v9wnBhWxZBJVhJvfTABC0do7c1sW87ND1+yb1CC7gN3Y5B/pMS6dqS+LTRr1axEQZicEblZFxCUqCuCG//3UxySQA1XoXHFyk1wWw/OCwArTAqxa/+GEYBEGXdNVnJcwexZVhPkOK8JfRde51zxyra9y7/rX7SwIMNn3AUQYMz0KZW5kc3RyZWFtCmVuZG9iagoyIDAgb2JqCjw8L1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA8PC9Qcm9jU2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQovRXh0R1N0YXRlIDw8L0czIDMgMCBSPj4KL0ZvbnQgPDwvRjQgNCAwIFI+Pj4+Ci9NZWRpYUJveCBbMCAwIDYxMiA3OTJdCi9Db250ZW50cyA1IDAgUgovU3RydWN0UGFyZW50cyAwCi9QYXJlbnQgOCAwIFI+PgplbmRvYmoKNiAwIG9iago8PC9UeXBlIC9QYWdlCi9SZXNvdXJjZXMgPDwvUHJvY1NldCBbL1BERiAvVGV4dCAvSW1hZ2VCIC9JbWFnZUMgL0ltYWdlSV0KL0V4dEdTdGF0ZSA8PC9HMyAzIDAgUj4+Ci9Gb250IDw8L0Y0IDQgMCBSPj4+PgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQovQ29udGVudHMgNyAwIFIKL1N0cnVjdFBhcmVudHMgMQovUGFyZW50IDggMCBSPj4KZW5kb2JqCjggMCBvYmoKPDwvVHlwZSAvUGFnZXMKL0NvdW50IDIKL0tpZHMgWzIgMCBSIDYgMCBSXT4+CmVuZG9iago5IDAgb2JqCjw8L1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDggMCBSPj4KZW5kb2JqCjEwIDAgb2JqCjw8L0xlbmd0aDEgMjIzODAKL0ZpbHRlciAvRmxhdGVEZWNvZGUKL0xlbmd0aCAxMjEyOT4+IHN0cmVhbQp4nO18CXhURfbvqbr3dt/eb3eS7k466b6dTjqQJgSSQAgEaLKBRiCsJkgkASJBQZYAiqMSZkQwLuAyuI77gjqMnQVsojMgOu6Kow7uiojbzCCojAtL33equjvAqP+X//ve+/7fvG/65vzq1Kmqe6tOnTp16l4RCACkIIgwZHxVdQ1yxwDIPpSWjK+bPG2t8U7MC5di/snx02ZUGP+kvwbLI5gfMnlaYdHFw7a/DkDvxnzTzKqJ9XU3nP9PgJzjAPab5i1uXkrGkaew/Cwsnz5v1Qr1nsy3/g5gvhhAN/28pQsWv7y64TYAx8uYv3BBc9tScIMB71+O9ZUFi1afN6N+YhHA8E0A6rut8xdffNPNE7xYdymS3NrSPH9f6rN4P5qK9Ye3osBRbNBhe+wj5LQuXnHxotHGOhzcCMwfWbRkXvPCs1bgvQXMwqWLmy9eKt1iacf6rH/qhc2LW1xNQz8AkAahrGrpkrYVWj5sRn4RK1+6vGVp7t6JOwHS8R6mPwG7kQwU7EA0DXmmy9HwDZTD70CPcgUKYSY+/fdYV8I8fyyAlsfu+TM/bK8fE5sElQocfezoJQqXnPYbzSVGGIyX1Ly8eS6o81YvXwTqguUtF4Da2jJ3OaiLmldcCOrJe4I5wVPQJWQ5eBEIwiDEwVCMOAxGIJbjRXgbKf222J7znppjK/+n7JF5s3s/yctn6Ut1o7YffezEAgVkdmfDKb2kEFduakIbqWhXYd4DpicRxsEZUAczoAH1BZirhFqYynLaJ8nrX8YsCBvIJtSeLN0mFWPXPfFU+AucRx2yRE06kbKfCP+irYmTJ03GZ4+DBumN2BRSrB9DusJsovDJYlB6gs0osFZp/3cuUo3XYfoHwSesEy+QZOkB6QHdS3qP/KLhT8bLTapJNa+0Zlvvs02KX8rixFxWwGwQ+CwOis8in79U3jfA3hKuuSRPTuFRDRe0LMe6p2JCD6weRa0TTm7eSg9nQhXSGCiBfESCkhwYiFZajPNfinNPIUdrhSLtPeRKEcuRCJcx3MilrSht1f3ENP9nf9JM7QRPn4PzkO6UZsK94iewRVcGizF/Py2DnfF6sFlsg826R+AWlN+B5fNQdmei7T3Iz8Z2Qxh/+v352tHDLGbZIvooOB/aEzzBWVyV4ClYoTXBC2h/AxK8eEodCTKwVpzXIcdWwnJYCM2wCCbCdPQZLZhvQ8kSYCt5GK7RoTAEyydyyRJYAathKdZScT0tRvkCrHshogoFSCfvpuLqakH5SuSbUXp67mS9h7FmET5hKF4q9qCV3/unT6vE3HLkGTajPN7DwfyZixLPW4hPaMWytsTT2/hoViHOx5qAtggQNslyP2ZVBr1ep5P1FPSIso5l9VxuNhj60V4PBoOsNxjQTSMaZGA5LreYjP1obwDWyojtDXqTwciyvL0BbGZTv9qbTEaDySiAUTYZzUbAnJHLFYv5f9sa9xgwm7GdSQCTwWLCR5pMBhNvb7dY/hvtpX9pb4IUm7Uf7S1gtVrMNosO9WWz2DBrMbPnmiHNrvSrvc1mtShWNHKz3apYwWY1s+dawZ3i6Ed7G9jtii3FrkN9pdhTFLArVjvKFfC4UvvR3gGpqQ57WooMDpsrJc0OqQ4lhcuzXM5+tE+BtLQUhytNDymKK82F2ZSUNC5XPe5+tE8DlystNd1lgDSHx5WO2bQUF5f7Pen9aO8Et9uZmuE2gNPhcWdg1pnm5u1zfZn9aJ8OHk+6K8tjgPQ0nycLs+kuD8pdkB9Q+9E+E7zezAy/1wyZroDXj9nMDC+XD84N9KO9D/x+X2aO3wy+jFx/DmZ9mX6Ue6FoYLAf7f2Qk+P35eVYwZ85MCcPs35fDpcPLxjYj/Y5kJeX48/Ps0GOtyAvH7M5/jyUB2Bk4aB+tM+D/Py8QEG+DfLUwvwCzOblsBAoCJWlRf1oXwBDhhQMLBmSAgW5pUNKMFswcAiX144e0Y/2RTB8eNHgkcPToCh/9PCRmC0qGI7yoTCtekw/2uOWXl5aPK7cBaWDq8vHYba0hIXWw2F2bXU/2o+GiorRIyZUZMDo4tqKCZgdXVbB5fOn1fajfSVMmFA5etKETKgcMW3CJMxWjpmA8gqQeiEdKUN6CNLFINsTtM+RvmBpbKH2BStnKf0bVo8mCGALbCULYSvu5bvJYWz1GOyAHngeDboK7oBL4SZYjzvqLJRchXvPVNxpq+Amkq71YIxzD+6498ArWPdsuBx6wUnc2pewBtYJb2CrdeissnEXq8Md7VpylrYSo7KPxN+gCs/CHW4padfqteu0G7T74QHYITyP0YYJd/F5eL2ifSW9rb2Pkzobfgu3wkfkBsM23PnPxvhgh/A73PtuExpFoi3QjmIP/HAR9kHEvfUVsouG8O4t8Dlxk0uFSrzLfVpEewZrZUIj7qG3QS8ZRsZTvzRbm6i9gu6gAC7Gu94KXbAdryj8Ed4lZumwdr92GBf7IIwG1qA+XiW7hNiJtbGxqDEJtTQQyrBkCfwJnoPXSIA8RZdIZqlICkuXaG9ixDgUI/Kz4SFs+Rn5nl6O1xrhWbFGq0BHvQ6uZ9qGP8PHJIMUkslkJh1Il9A7heW4DQ/iEcN83POvglvw7h+SENlOzXSPcJ/4qHhMlxXbp1lxRoJwO56JniIWHKlK2sivyV7yCa2kc+jtdL9wk/iw+Lq+GUd9LkYz18Kj8D1xkBFkCjmHtJJLyXpyPbmVvEJeI1/QcXQ6vYAeElqFZcIfxQq8polt4m+kK6WrdV/E6mPPxP4S+14r0q6EKWgPa7H3v8XorgftZA+8g9dHsJ9IxESseKnET2aQX+F1ObmW3Eu2kIdJDz7lNbKffEm+If8kxygGdFRHPdRPs/EK0OX0InoTvYPuwes1+g/6o+ASsoWQMEwoFxqEJdir9cImvLYJH4sZ4h5RQz0XSZulu6Qt0qPSbumwzqz/tQzyy8fvO5F/4sMYxDbENse6Yj3ax+jW09GmMtFtlmPvm/E6H+d7M1rcY/AGMaPuMkg+GUPOQs3MIeeTZeRi1OQV5DbyAO/7H8iTqKW3yCHss4Vm8j4PpsNoBZ2M17m0hS6jm+gNtIfupUcFvWASbEKakC+MFxqFFmGFsFrYLESEl4UPhP3Cd8JxvDTRKPrEbDEohsTx4hxxpXin+Ln4uTRbekn6VGfULdZdqYvqvtYP14/R1+mn6Bv1G/Xb9W/KTWidT8M2ePxUb0D2CWuFamEbXEeLxXT6Kn0V7XkOzBcmUrRUuoVsoJeRHpojXawbRUeRSXBYDKKun6V30e/oKGEiqSXT4Hw6NH43Xar4CCbl4tNwUHwSx/Yq3vlinZlcTg/pzNCFx6YyfOafhSFiSHgJ3hU+InrxHnhPNBIXOUgfEurQCv4ojpHqwS/cAX8QlpHLYBtFt2g8Jl+DdjyJPIJ+YTopIj8IeLqnk9CKSoVP4DdwAX0bDuI63gA3k/niArgOisml8Dk8iKtioHShLl+XRl6gC8UOmkJ6gIoP4+jKSA4RpFS4gjQKt+kO0XcwCt8jGuFD4ffY+z14bpwoHpamklZcAZfBlbBMWwurpXrxdbIABDITcsV96N0uFYpEP6Zr0KvMRp+2HVd3L/qBccJElLjRcs5Cu5iBHuI2vG5BPyGiBS3ENX42erFXoUc3nUZhgWQl6HXwHPxSbCrM0h6EW7UFcKF2AxSgP1ivXYp33AKfwkbYQtbFfoXxvhdXzofkLKmG7pFqtALaQd+h0+jm0+cXtZ1L3PA3vP6AmTF4xu4Q34JpMFa7RvsrWvcA9LC3wlw8gR7AUX6FT5gg7ILi2CTaqdUIS3G8H8EU7SHNR4zQqi2CyfAkPKCXoFkfwjmOkNdxvL+CFjpVWyG0xBaiHjaiFsKorZXof64KV86YPi48dszo8lEjy0aUDispLho6pHBwwaBQ/sABecHcnEC2X/V5szI9GelulzMtNcWB0SWGtBiVy3qdJAqUwKDqQE2TGgk2RcRgYMKEApYPNKOg+RRBU0RFUc3pdSJqE6+mnl4zjDXP+5ea4XjNcF9NoqjlUF4wSK0OqJFXqgJqlMyaUo/8tVWBBjVykPMTOb+J8xbk/X5soFa7W6vUCGlSqyM1q1o7qpuq8HadJmNloLLFWDAIOo0mZE3IRVyBpZ3ENYZwhrqqR3ZSkC3YqUhGoKo6kh6oYj2ICLnVzfMjdVPqq6s8fn9DwaAIqZwXmBuBQEXEFuJVoJI/JqKrjOj5Y9SFbDRwtdo5aFfHNVEF5jaFzPMD85tn10eE5gb2DHsIn1sVcV1ywH0yizd3VNavP7XUI3RUuxeqLNvRsV6N3D2l/tRSP8OGBrwHtqW5NU0dNfjoa1CJtdNUfBpd11AfIevwkSobCRtVfHwtgWomaTpfjRgCFYHWjvObcGoyOiIwdbW/KyMjvEPbBxnVasf0+oA/MtYTaGiuyuxMhY6pq7vTw2r66SUFgzoVe1yxnVZbgjFbTmVa+so4x6szrnZqn2YJ61HgDDSIiDpPxZ7UB3BMIxi0jICOeSOwGv4aCLaKzMcZWRgxVDZ1KCOZnLWPSLlKQO34J6AFBA7+43RJc0Kiy1X+CYxldtJnalie5COhUCQ/n5mIvhLnFPs4hueHFQxaFaWBwFJFxQTVB3Wo2+aGkYWofr+fTfDV0TDMxUykfUp9PK/CXE8XhAtDDRHaxEp2JUvSZrCS9mRJX/OmAFpyD3+jlBaRg31/NsWZUt06MkKc/0VxS7y8dlqgdsqserW6oymh29rpp+Xi5SP6yhJcJKWyXvDQBEc9Ai9Fo5zdV5ll6s0RMRf/dNyo50f1MlollxC1JqI0TYhjg9Hv72ejqHaYteLJyWaJbkZGhk7Pjzotf1r3zB0Cdhi3ytrpszo6jKeVoanFH3hGIkGLh+n1frUyAjNwZebiX1TbNYJRgycSRpVVsgpof3FRIntaRU+Cb8Afs86CQTXo6Do6agJqTUdTR3NUa58bUJVAxw66m+7uWFrdlDScqNZ7tSdSc00D6qqVjMRFQaGiM0A2TOkMkw3TZtXvUADUDdPruyihlU0VDZ05WFa/QwUIcyllUiZkGZVloJbgILuozOt7doQB2nmpyAU8Py9KgMvkpIzAvCiNy5SkjKJMjMvCXMZ+zMdUTq8/1Xr4kmwoAAwppwsDuoNu32tPCgNhHxIVBnaFsnw7hDwhq2uULxwVAt2OtCLbuAJBxWcWclQRlyA9hrRTYO+g5whelCuIa5DakR5D2on0GpIOAJGVqkhLkO5C2sdKhCwhs0v1KePyhHRsm45jsAkuOISkIQngQyxEmow0B2kj0l1IOl6PSZYgrUHaiXSYl4QFV9cNxdh3V9fVPOk+f1ERzzbHs7Mbebb77IZ4OnFKPK06I15tZLza0JK4eHBFPM0bFE8duUXtLDVainaNcwpOHKQTO74UkdBnwEYIhjF3C2kQQaKCLiEJC47unGDRXTsFEYhABYLHDp+2SyBdFnvROCPV6CFwgI9+RQ/GS+jBbqu96K5xZ9L98BjSTiSB7sfrY/oxrKH7mM4RxyLdhbQTaQ/SISQd3YfXR3h9SD8EG/0ACpHGIs1BugtpJ9IhJD39AFGh7zP/xJHxY5EofR9Roe/hsN5DtNF3kXuXvotde6OrtKxoB2dChQnGl5tgXJ4E43AWRenrXT8ORIsK4kyjRT0hZMMYKBayu3KH+qKCu6t8oS9KP+lWQ767xw2hb0IEiWJP3sQnvwkqUh1SE9JSJB1ye5HbC+1Im5DuRoogoZUhKkgqfRHpZaS9MAQpjFSHJNPXuvAxUbqnK1jhG+fEAP45PEz76Cv0eZ6+TJ/l6Uv0zzx9AVMvpi/SZ7u8PhhnwnLANgqmCqaFWC7Rp7pzHD5tnJ3uRN35EAuRxiJNRpqDtBFJR3fS7K75Pgfe5Al4UQas2QVf8vRBuFeG8Pm+cLASDVBlEBw5GjmEu9S7gjQc3HwrZhkEr7sBOQbBK65BjkHwkrXIMQguWoUcg+D885FjEJw1BzkGwcnTkUOI0jsfz8nzlU6+gKjjbPQi1NJFqKWLUEsXgYjnQ7zgR5H17fau/HzU2G3h0MB8X3svaX+StE8l7feS9hbSfjlpX0vay0n7uaQ9RNozSbuXtIdJ+xOEfYprJ+Ge07JlYTdpf5G0byXtbaQ9SNpzSXsOaVdJaThK/V1nFPOkmifd49iiw3T0GPQ+NupHjfrR5v3oE3Yi7kHSeC6MldTseOV0L0uzu/PHxvODRxYtGTeBPo0Nn8ZpeBo+QhJxgp5GM3oab/I03sCGOBZpDtIupENIGpIOa2djxzdytCEWIo1FmoO0BukQko535xAShSWJLj7GO1aY6PRklqNP48UO4H7qD2cpmUpImSBszCQ2L5ns1by0FJzsfa7DLtujxLL9e8sP31vAMM5Ar6MbIQsnYlMi3dj1Y5YvSm7pCj7hG5dGbgaviFZHyiBIcjEdAW08PwwyZZaWQCZ9FNOirsyZ2MzWFRzk6yVW1mq778fMA74vM6MU2S8yn/C9pUZF0uX7K0oe3e57M/Mq3wuFURklTwajBJNelVfdkTnCt/VFXnUtFtzW5bucJdt9l2WO912QyQta4gXntmEubPNNDc7yTcD7VWXO9YXb8J7bfWMzz/WVx2sNY222+4ZgF0JxNh87OzCTPzTg5TecURolreFB+s36ev1kPK0X6Qfp/XqfPkvv0afKDlmRrbJZNsqyrJNFmcogp0a1feEQ+46YquMfonUi/6jIeYUC/yzJPzVSIlM80kVShFpaO62C1EZ2zYPauWrku2mBKDFitCIFKkjEUQu10ysiI0K1Ub02NVIaqo3o686p7yTkugaURugG3KWn10eJxkTrPOxcsAMIsa+71sPSAeuubWgAt3PVWPdYxxh7WU3Vz0BTAkMnf+7T+KzI5tpp9ZFHshoiRYzRshpqIzeyg8MO8g05XF21g3zNkob6HcIY8k31VCYXxlQ1NNRGyUxeD1TyNdZDi/ma15NxY2b1QJW98Xq3xevlYnusl8MSrGcwQC6vl2sw8HoiYfU623KqqzpzcngdlwptvE6bSz21zou5WCc3l9dxtsOLvM6LznZWJzKGV8nMxCreTF6FZEAmr5JJMniVmSerFCaqXNVX5Sr+JIGcrJMZr2PZl6xj2Yd1Qv39tVSEQqR7VMO82ezQ1RSobkFqily9qtUdaZ+rqp3zGhKnsWDT3HmtLG1uiTQEWqoi8wJVaueo2T9TPJsVjwpUdcLs6un1nbPDLVVdo8KjqgPNVQ3d4+tKSk971lV9zyqp+5mb1bGblbBnjS/9meJSVjyePauUPauUPWt8eDx/FnAbr6vvlKGiAWN8nnZTkxHttcnjb6hwKkvHcOMd5Xdf7unFaGULmPDIY8bjswWJFRWMKxjHinBNsSIrO1knityXj/J7esmWRJGCYnugAkIrVratBHf1wqr4Xxv+ULRiJVN4HENtv/TDsmo8JFe1rQCojeRPq42MxWi2U69HaRMbUmRkUmYyVWNsHxcORuFIJhSEvopMVs5kBkOi4k/nf2UirWSroJ0+0U3CXrIC2hqEiLd2OkVXMD1xhOnFWIptD20NOMA2EiJtyXskuh0KQTwPbMxJWrEywSV0sSKRxltik7akSvp+TFmhPo2twBuynwACYT9JEAjFMNMt/cO0C36QNUAXqMXYB2DtBBjByN/3mxDNYEa0gAXRytEGVkQFbIh2xOMYhtoRU8CBmAopiGmIx8AJqYguSEN0Ix6FdHAhnwHpyHsgAzGTYxZ4EL2Qqf2IoS9DFbIQ/RjY/gjZoCIGEH+AHPAj5kI2YhDxe8iDAOIAyEEcCEHEfI4hyNO+g0EwALGA42DIRyyEEOIQKEAcivhPKILBiMVQiFgCQ7QjMIzjcBiKWArFiCOgRPsWyjiOhGGIoziWw3DE0VCKOAZGII6FMu0bCMNIxHEwCrECyhErEb+GKhiNWA1jEGtgrHYYxkMYcQKMQzwDKhDP5FgLlYhnQRXiRKjRDsEkjpNhPGIdTECcAmdoX8FUjtPgTMTpUKsdhBkwEXEmx7NhEmI9TNb+AQ1QhzgL8SCcA1OQnw3TEBthOuK5HOfADO3v0AQzEZvhbMS5iH+DedCAOB9mIbbAOYjnwWztS1jAsRUaERfCudoXcD40IX8Bx0XQjLgY5qL8QpiHuITjUpivfQ7LoAVxOSxAbOO4Alq1z2AlLERcBecjXoT4KVwMFyCuhsWIl8CFiL/ieCksQbwMliJeDsu0A7CGYzu0Ia6FFYi/hpUae4+9CvEKjuvgIm0/XAkXI66H1Ygb4BLEq+BX2sfQAZciXg2XoeQaxI/hWrgc8TpYg7gR1iJuQtwH18OvEW+A3yDeCFdoH8FNHH8L6xA3w3rEm2EDlt6C+BHcClch3gYd2odwO1yNeAdcg/g7jnfCdYh3wUbEu2ET4j2IH8C9cD3ifXAD4v1wI+IDcJP2PjwIv9Xeg4dgM+IWuBnxYY6PwC2Ij8KtiL+H2xG3cvwD3IH4GPwOMQJ3InYivgtdcBdiN9yN2AP3au/ANrhPexu2c3wc7keMwgOIO+BBxF6OT8AWxCfhYe0t+CM8gvgnjjvhUcRd8HvEp2Ar4m74A+LT8Ji2F56BCOKfoVP7KzzL8TnoQnweurU34QXoQXwRtiG+BNsRX4bHEV+BKOKrsANxD8fXoBfxL/Ak4uvwR+0NeAPxdXgT/oT4V9iJuBd2aX+Btzi+DbsR34GnEd+FZxDf4/g+/BnxA3gW8UN4TnsNPuK4D17Q9sDH8CLifngJ8ROOB+BlxE/hFcTP4FXEz+E17VX4guOX8BfEv8Hr2ivwd3gD8R8cD8KbiF/BXu1lOARvIR7m+DW8jfgNvIP4LbyLeITjP+F97SX4Dj5A/B4+RPwB8UX4ET5CPAr7EI/Bx4jHOZ6AT7QXIAYHEDX4FPE/Pv3/vU//+t/cp/+93z79y1/w6V/+xKd/8Qs+/fOf+PTP+uHTD/T59OWn+fRPfsGnf8J9+ic/8en7uU/ff4pP3899+n7u0/ef4tM//olP38d9+j7u0/f9G/r0d/6HfPqb//Hp//Hp/3Y+/d89Tv/39em/FKf/x6f/x6f/vE9//v8Dn075Pz7CCwTQA/jtfnsuAvvnLMdVYdfxsIQ3UMVdAJT9iw+pQerFelaatQOI9kOP2VwxwxjVjnPGEE1IpCQjIhN2MU6WGepEhno5Uelo2GQyYZmOIdY9Es9TM0PC8uMYpzMy1DsZAi8z6fiDjfw+HA1Wfn/O6zlPrDaFzqBR7ZueBPNDj8WiY8yRcIPZrJthMDOUOBYqQ5QFcquhSdkgbFJekJ7V7VIOKyZZaiAzaZ3Saooo35q/tXxrNYhm0SJaBZPRIImi2WKVdXq9GXlZZ9ajMtmIbWYznQGq3pyKRVQQmCyNyQRVNKdiK4NXkmSvTtBF6dKwAWTzl2FKKO0lJiDEFHaYVWjRC1PrxD3iR6KwSSRilJCwqc68S/+RWdhkJmaWV2z6PXq6Rt+up/obbXvfcoeUI43L0pHwz31QOZiRrhw8CO6x5RkHxx4oVw7i33ppcCh0mfLM+sFunhK7o6zMXla2XnnmGeszz6yX4unQIaQ2YppWG/FOmVXfI9oEWd+L+wtoP4zAXwNZvqzxv3ojHSDFJCD4hRS/EMzT6QVa/Bda/8GjJ26/5x3y9a012ZnFUu/RGvJkrIrOIpt3XHTt1ezTxnna59Iq6Q3c5Q9tm0fPz6JoAl/0mEy6GajVL8JzGKdCkWUe7gorstrhiqxNcJv0qPCAZYfQY3nO8hocyPo2y251ZNmzsoR83QB7fqbqG2+ZmXp22sz0VumCrF85rnbcJtxqvS1zC7mfbrH/1ZqCkUiGkqpkiGgXH3YNKMNn7gpXDyhTbEBET4rXLHi8okEJ2s6EoEoIyfC5KDMvl5UZostotiAGVZmgUSMrm1kv5XTvvNnu0CTlSCjUOPEgamSS8h0yRw7C2INjD9pdZahgLGpcBqhHspy4dGIgO4cOK3HkFBeJLn0wGMjW0bRUh7O4aLjYs3t07OlPD8beuv0xUrn7fTJo1M7i3Tc+/MnsxZ9ded9+SoceOvYUufD1T8mMzn0vFdx9w72xQ9c/Efuy40n2LwTvxFU7C1etDbJIetih+kilnJnlRXuzK14byK6oFuOL1cWWCh9UVPsunJ0YmIH4whYLnWFQFVxFBqPNhujmEraQ8vhCyvBlKVwfitGCzRQzu5+iEv7fX7B2OIHf9bCmnGGtkTnaw9dJVPu+h92FLx0jW6LQ6B2F6lO+i1tTY/kJxPJEtpGpE8aWnyhnNHRI5erwcMGjl3WyJIuyqEt3Z7ipjv3zH4tR0KU5U50pTkHnEVx+4rAiuOVMP3Ea7X5AzYdC+fhbSxqL7f4il9PldKSlUisN5PqLhpcOHz6sJJgXDPjvJD8+OuvyhhVtky65/pV1sU5Sdv0DQ6sn3rxo0tbYy1JvWtZZc2N7nnkoFnu4uWjr8KHVXz742ff57L8xuRdAZP9tvQl6wmk6ySvLej0IIlO+0eA1gaxn1laoOEr004UzVaNqocYMi2igcZfGNGrgFmboty6P9hgMfRKu1MNJpZpHnZOwyYRaJ3K9ctM8cuCkTh1lheUKUy0qJc2foHvFnON3CqHjfxWukHq3xsb+PmbZij3agiNchyM0wL3h0XyEG/Wkb5A4wDtUqpoozTD9H40qbOLDMiecQOwnYzKOmv2LYzoAYxPDafzX8WwRPjj+KY2cqGNjGbn1xHnM/yxG/7MD/U8umRTO8KR60mhTHjlXTiEOIQfPEw4XzQUv5Q4ijfWDEJ3LaxX8Xp2BkGBebk5yJeUkV1IOW0kKG2qOKgioibwmKqCjOcBHyvcmNlJk3uXzx/emYnZvurw9j+RlcZVlcZVlcZVlBVUjMXJXY1RYRWN6cN45p7maiUrjdwldKFwZ6OILud/BNIQKwTz+Mc/vKOPrp0oMeDIzMtMzBZ05qOSmBX1BOVcMBnLdliw/OG0pfqycmqLqMZct5fpJpgkXUqodwWvw+yFHQOAfjnBBKeVKed9GwJYWNJJhufbTHJzTpR9M0cPp9Dr0cSL6uFK7cBZdvDH22t1vx+7q6SZ1791FyA3Bx/xzty9Zt/si/4j1hF5/+eExdOzvyYl9y9t2kHPf3kvaehZEbxqytH3ilCsmb7jrmdgP7c2lxM7m8n70etls5RHzDjyO7go7U9JKRMFrMN5tfM1IjRKlJhk9RnLK5OSUyWzKDNyVq3q9Lqp9xecKmW/CJjZZOoXNlI59r89nZqkjbBp0je0WYqEmPmEmPmEmPmGmuI0zozFiF/ph7HLC2E/xis7EAlYtRLXUWZosSy3iqAZ3qHFZ0kee9JLxyUeGZ3FRjy0vayzkrpKEiu24BpACiPfvpkd37z6hk3pPPEhnHa2h3ScmYk93ovrWouYEkh1Op3w8AkeqZ6MS9Ing7EeuLuzej2E7j9okNlyBIxYf62EMFh8Lcz0wZ0Ax5tvVPWJ0CU+LS+JpwZB4OmBgPA3kxtMsbzx1Z/A0nG9RSlRpk/SYhEsJI62NePiJgFiIZ+g6jMYPg+RQUbgJBF6dTxa4E+r+R1LdXyXVzRYmD9O4uu8V9zacsuNUzq7vasdYrLFh2fLyE32xDqpzLN+5kz+mz527WTCDmtuMNjeV2RxNCXuF7NIy2TAyzzhMN9w43ni2cKXwlqBfZXxHeAe3JbbO+SY6QLpG7JAeEf8mS0aRDBP3itTATMvg8JcIKgMMS7rNZQ4m7ca8nEhFlmbxdFe3w8nkH4ZHp+Mzc3NHy4b09NG4ugxGg2yUBFFUJWOqJGEOjVqHUanOaASJigTnVAbZKFATRvxROjJsGyKRu6WItEvaJ4nSmTKTmYboiYpRZkQv6KP0yrD356y839tTwqi/ObkrbWGBa+jk5n6icdlBjGAPMk9Sziy4vJwRei8WvVpZ9Cph+Coio5eVcrkcY1U3xqoejFV3gKi9PaKhU8f+M1KWOdxttjMlHsZziL1Ep1jtJbJiVUoMjDMqaFOJL94NJycWZz9sN2SjMgell4mMsj1laFQfbnci6yzTMV2bHGVydmqZGE4tY7rflotsWtkpQXADuzFZtrwxBCxaZqZC/AT/9PbNu+nbRH/iVvprDU58dxhX4ED61ok/HL+Ffva3GP8Pf9CWxHy0JQl+HTYTip5LAlllBwH6UNivp/ElKfApEPgUCP0OEb77Sbil+7lw67PGeETA9k22c2KnX0dL/3Yr698tADob9k8RXGGznG/CDlCOnTSueRkXGPdnstVi5zsbrjxkUI1fhQcwzuxgxZLNLBiAUNlgsoJsoEaTjo3ApLBem7DX21ktk4Ld/awnMbYfkmM7Hh9bIfb3FQ64PnftUl57bZfd4cK5iE8peOLmEPbp+WLXcRQ4ihwljmwPCAcYR3nAgbsh24mtJ8+KRo765FFSZir0MS4oEbNqdJTYOEhmAYgVwzsZ4zw2cHY3zvCbPEFnggMUOjNsSUQ2uuSE8NsCYWM5UniEx7lo+vHBNJ7ieeI26wmvAWqTU6lHFleZrzQ/j6o0n2E+wyYMFHMtg6z1wjniKsvF1vUW2UQlucwy3DqZ1gpV+rA80VJhNd5CbxU26zfLW4SH9DoHtVmtQySKfoLKZotliCQjK5un2qaSMB5OZdmA53CLxWpV2Dw1Odod1NFLt4CFDO2SVDlKhoadZoORH9bjR3OjGjavMRFTLw7YSkxYi0YxsRFuhIntg5sJcqptqUKUKJ35uCo1Se0SenG6pdvOtrl0PNceaSx3n2BmyU+1mMs4JXugEU+5qCjllCsDz77MX6y/jB92MRk6BE4eav8IZu0YWuleoNpefqatjZixbAB3Ihbth06rkUn5f1Rj0d7c7i+zDvKXWaLIlpZZi0o5u60ApQWJVd+Ap2Jc6rhpsKWPS4Y4XcNLiR93WxIg9ltIDjlniDN9GJlDpCdiMx+L1Uu9x765fkLd7cLxozXiS8eGifuOqWx13YE7iY9F1eTJ7YI7EZ98sY0xDlMylJDdZiedIbCjcRbjZIr7ol5G7y5TvSDIBpFSg14WBb4ZM2+RjHGYBGMcJlJ1Oim5O0p9MY4UX5oYg4SDfH00qiaimupMTaalpnaTZJL7wngzD+N5fGPBTvUvnhd/GuL0xfOnbMOhxlA5n+TGZUf+NaZxlGEEW1a2XuQznPT3grbvcXTzsooA3KezmBTnsEcO15ThuHdtrymTw0VxtqhMj06eHfy3pyNbFGeZNMDZsClQpremIqWw/JHtKchmxdksZNMY+0Nnn9cnpyzOuAkUExZsEfsdzwm097njMZzwteIanOz2Y+3sX0DgieMD6U2wgoc4w7UZNpKqpKZ6XB6PKCpiqsll8ogPu7Zbn7UKLpfbQ9WssH1yymRXOKNeqjecrcywz0mZ5Zrjnplxtudq161USfcKgsNrMqQl49q05JynsZXGN4q0oIpHNBwDl+vZOxY2YfpkbITMYb5VIPM37rp4ZTY/ejaFY7kPzGjPIlk2vgvZuC3Y+M1tQWYBcvxVHY8Adad4uPTMeSePa8kXI419sz0xfrTHkwq6OvZupLFxWYoC/iKRHcv5AaJUgeIisJfQYCAb5pENZPhLpObRntj2nXtivVueJ1lvvUc8q7+8/tXYW/RFspj8bnfsgfc/it297Xky60+x72N7SAnxdBPTjbFP4+9GxBO4zizghsNhb4v9glRaq9SmnqOckyqazF70iOByx0+yjqRKHUmVIvPDdva+wxHkpwY742Uj06GsJDaUI+ECNnI5Q80g+JfhtnCVWbjKLFxllv/uKfinJ/v0U/fv5AY+SVkWV21CrcmjPT8J4KmMv/LwUtSs329Hvu9tBx14w8RFNzR8FXshtoH86sk7G88aekXsKqnX6mjZvviJ2IkTvxfINWtm/ybNwt4v3YO+aivq0A3ZGCv6HSYrcQzPnOU7T17sEw0K3yc56jnikXgXty4LMyrGmJOMKcmgYvd3OzJKMD3cnZ1XYmf5rLwSJZHaEimWv92dFYyXY30lkbLy8BnI5FrPzDxTnWaanbk4c7nhYutq2zrjBtvNlodtUdsX1s9tCu7tqt2Warfb7DazweGh/gynUeewKxaz5DYYnK6MdK+L9TjxXgxP/mwSXC7wZ3OzcLttNqvsTdqGN2kb3r5jpDdovUPHFlniGBmfVn5+LOEnSR1Ti65RzVma054j5GS7uYW4uYW4uYW4+2shul/0qwEWZf/0PUli8aUfcCfeqrGdM2EoGIhjpqwQgw9id5Wttw4OSRhyM+MJnfqDxIEpbJTDtjKbMtLuGMkcIFnG904r+tGM9DI7eloHkjWcWaZg3Kxk+5D6XGcDs0anMy1Vp3e6nK6UgDCYojEGuGEyywz476Edz7x8yYtvTBww4yztyO4ZF55d4K/9mNyzbvOkm++LDZF6Jz+/+o69Wbk5k1bGlpGhV1wzwqQ/sVIoLl09vvVKtqvO1j4X/y69AUPon3dAHg+2KmYEowkml3+rYJxbYROQzjGDoyX+IrqC2WqcMSWZzCTjYRvxaL69uvl5mCPhOE+YJ7YJK0QxN2+YUJZZKZyhPyur2leVU5M3TWjQz846e8BVKdYAMx42xzlJJjfJBJNMXpIJ8OmPV44zuUkmmGTymBHWMG6AJZhDc4S83OG2kkBVbnXhLHVmYEbuItP5lgus56W2uFebLrFcYrtMWZnTlnul0GG6ytJhu1ZZl/Ob3Bssm22b07yJELrAH3R4ghmG4EASBBiY4RCLhgahBf2ApWC15yoP9eQ6LQXevFySKzkl5v/iH1m8BQav1ylw5x6yO8oa4y+hWNJIWHxbeDB+ecIFuTlWi0nyZ2Z5PbJeJwpUR3JzslGmk7yegowwM/WN6EsPOqGAv43j0YpCVFJHmshSsonoSJREwtYC9kj2aOzxmYa4d+GfqeJr1JBYH8gFYSAZyLY7q5XOGMi67WP3HJhR5Ofvsv18NfplVhk1QIIOFjSxyo7kMnT0fflxTGerNX1o4r1c48QDaOAHlcRngOQ+l/gWoJxoDB1gcIRpAdcZ+yBDkMXYBRqXnVxm5NQMX3QppV5aXJR4S52TFwwOKxk+vBhXUeL7QVqqyym6+KLS4d4ZnP24Zc7zly15ZFrd7FGxRVMWLrj8m5vu+/FKqde29eHIPWUjyDv17Zdceex3z8W+vZW8pVx47dkVbVXVCwKu5lDpfS1Lnpq/8OW11quvW3vO5OLiCwaM2rZq5Z62FV+ylTUE99Fe/mXww3C6jvsvPUcdf1uk/6V3Rjr+tkj/M++M7IyTqBdnH/j/LMAQpW3davxL2OM6ldBCgQjIbyOJ92tfhE3cP8oJ5/hN8ri7P+kljye9Yix+zGJ3lLffeurJF2cLg8wDjZ8xPxjfMk973+O3+4ex98c0JZYldsQ8kmXr1qPf4vPvwUiOvW9MJeawMWirF+vlF2TRGU28eSwRR8k14pnyKtuD0hc2vRmoPUqf6NIZUpM7R2rSKpH5bjsbfWqQJiNz2heZUyXxnnhfeDA/qTaqTqI665y0ybnU2e4UnD8TYPB3xsljg5FvI8bkNmJM2q+xbxsxionzanwbMfZtI8bGNBaen9xG4u9rJioYp50aaRwcy0OMEDSSYnsicBuGgXCqk33OsotNu+fHjr35auzo0t3jt162d7vUe7zzg9jx+64jli+Fyce7dm6bu5uksn8EhbFFDWrVTGkYXQJbfWaO3FgsfcbCuPg3YTNHEg+SKvr2xooZopiIdo8nX/MeTTqBb8Iu7rZt3LFzWzX/jMXGv1UbRgriKGz0ebfDxV66fR62IiOmIwgMDCwmcfP3dG+HRyEjDkBwBMWBcr6x0Cq2klZdq+lDnSiJgqCT9QadzqAT8CDFvq6pRlMqHqB1gs4gMN/tZFJBpSSVUqIzm3QElwMxRWl6GA/aBoHi4rBGqRsjDcPUsLHdSI1Rsg1VZTKrIEydTDdSSpnEQAikJsOHsIkvEXNiWexPLBTq3m6x7vY3YaAQ+i5+3DrSiP4pnnzGVgOesI/wtxHEUbZ+cCgkYzwg8U/JjFvPPiArCLURF56kM9mnY9lsMIu92hE8mR0h/Nsxc2uExwsG/ooNScSzVmc6CwVO/uuWUxZd39ojxfETNZ6q6KgTL/2D+OuqK84lmftPPE4XCxNjNZde2raJPHa8+8SNAPC/AG1JKkMKZW5kc3RyZWFtCmVuZG9iagoxMSAwIG9iago8PC9UeXBlIC9Gb250RGVzY3JpcHRvcgovRm9udE5hbWUgL0FBQUFBQStBcmlhbE1UCi9GbGFncyA0Ci9Bc2NlbnQgOTA1LjI3MzQ0Ci9EZXNjZW50IC0yMTEuOTE0MDYKL1N0ZW1WIDQ1Ljg5ODQzOAovQ2FwSGVpZ2h0IDcxNS44MjAzMQovSXRhbGljQW5nbGUgMAovRm9udEJCb3ggWy02NjQuNTUwNzggLTMyNC43MDcwMyAyMDAwIDEwMDUuODU5MzhdCi9Gb250RmlsZTIgMTAgMCBSPj4KZW5kb2JqCjEyIDAgb2JqCjw8L1R5cGUgL0ZvbnQKL0ZvbnREZXNjcmlwdG9yIDExIDAgUgovQmFzZUZvbnQgL0FBQUFBQStBcmlhbE1UCi9TdWJ0eXBlIC9DSURGb250VHlwZTIKL0NJRFRvR0lETWFwIC9JZGVudGl0eQovQ0lEU3lzdGVtSW5mbyA8PC9SZWdpc3RyeSAoQWRvYmUpCi9PcmRlcmluZyAoSWRlbnRpdHkpCi9TdXBwbGVtZW50IDA+PgovVyBbMCBbNzUwXSAzNiBbNjY2Ljk5MjE5IDAgNzIyLjE2Nzk3IDcyMi4xNjc5NyA2NjYuOTkyMTkgNjEwLjgzOTg0IDc3Ny44MzIwMyA3MjIuMTY3OTcgMjc3LjgzMjAzIDAgNjY2Ljk5MjE5IDU1Ni4xNTIzNCA4MzMuMDA3ODEgNzIyLjE2Nzk3IDc3Ny44MzIwMyA2NjYuOTkyMTkgMCA3MjIuMTY3OTcgNjY2Ljk5MjE5IDYxMC44Mzk4NCA3MjIuMTY3OTcgMCAwIDAgNjY2Ljk5MjE5XV0KL0RXIDA+PgplbmRvYmoKMTMgMCBvYmoKPDwvRmlsdGVyIC9GbGF0ZURlY29kZQovTGVuZ3RoIDI2Nz4+IHN0cmVhbQp4nF1Ry2qFMBDd5ytmebu4qNFbWhChtS246IPafkBMRhuoSYhx4d83D2uhAwmcmXNOZiZZ2z10SjrI3qzmPToYpRIWF71ajjDgJBUpKAjJ3Y7izWdmSObF/bY4nDs1alLXANm7ry7ObnC6E3rAK5K9WoFWqglOn23vcb8a840zKgc5aRoQOHqnZ2Ze2IyQRdm5E74u3Xb2mj/Gx2YQaMRF6oZrgYthHC1TE5I699FA/eSjIajEvzpNqmHkX8wGNq08O8+rogmobCO63Ebtzip/NccT9DrSaGJXZdTSx4jKMiXvk+ElJW+SL919k1NoL6zxmJ2v1vqx467jvGFSqfD4DqNNUIXzA8M8h6gKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8L1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUwCi9CYXNlRm9udCAvQUFBQUFBK0FyaWFsTVQKL0VuY29kaW5nIC9JZGVudGl0eS1ICi9EZXNjZW5kYW50Rm9udHMgWzEyIDAgUl0KL1RvVW5pY29kZSAxMyAwIFI+PgplbmRvYmoKeHJlZgowIDE0CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAxMDk3IDAwMDAwIG4gCjAwMDAwMDAxMDkgMDAwMDAgbiAKMDAwMDAxNDgzNyAwMDAwMCBuIAowMDAwMDAwMTQ2IDAwMDAwIG4gCjAwMDAwMDEzMDUgMDAwMDAgbiAKMDAwMDAwMDY4NyAwMDAwMCBuIAowMDAwMDAxNTEzIDAwMDAwIG4gCjAwMDAwMDE1NzQgMDAwMDAgbiAKMDAwMDAwMTYyMSAwMDAwMCBuIAowMDAwMDEzODM4IDAwMDAwIG4gCjAwMDAwMTQwNzQgMDAwMDAgbiAKMDAwMDAxNDQ5OSAwMDAwMCBuIAp0cmFpbGVyCjw8L1NpemUgMTQKL1Jvb3QgOSAwIFIKL0luZm8gMSAwIFI+PgpzdGFydHhyZWYKMTQ5NzYKJSVFT0YK')
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
                session.clear()
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
    if not (session.get('username') == email_id):
        return jsonify({'message': 'Invalid user data access','exception':  'No rights to view','status' : 'failed'}), 404
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
        mycursor.execute("SELECT student.email FROM student JOIN certificate on certificate.certNo = student.certNo WHERE certificate.certNo = %s", (certificate_id,))
        student_email = mycursor.fetchall()
        print("Student email ID is  : " + student_email[0][0] ) 
        print("The current session user is" + str(session.get('username')))
        if (session.get('username') == student_email[0][0]):
            print("The current session user is" + str(session.get('username')))
            mycursor.execute("SELECT student.studentId, student.fname, student.lname, certificate.certNo,certificate.document FROM certificate JOIN student on certificate.certNo = student.certNo WHERE student.email = %s", (student_email[0][0],))
            certificate = mycursor.fetchall()
            if certificate:
                print(certificate)
                certificate =certificate[0]
                return jsonify({'studentId': certificate[0], 'fname': certificate[1], 'lname':certificate[2], 'certNo':certificate[3], 'document': str(certificate[4]),'status':'success'}), 200
            else:
                return jsonify({'message': 'certificate not found','status':'failed'}), 404
        #----------------------------------------------------
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
        fName = request.json['fName']
        lName = request.json['lName']
        graduationYear = request.json['graduationYear']
        number = request.json['number']
        if len(number) != 12:
             raise StringLengthError("Incorrect phone number")
        role = request.json['role']
        statement = 'UPDATE student SET fname = %s, lname = %s, graduationYear = %s, role = %s, number = %s WHERE email = %s'
        values = (fName, lName, graduationYear, role, number,email_id)
        mycursor.execute(statement, values)
        print("Student data Updated")
        mydb.commit()
        return jsonify({'message': 'Student record updated successfully','status' : 'success'}), 201
    except Exception as e:
        return jsonify({'message': 'Student record not updated','exception':  str(e),'status' : 'failed'}), 500
    finally:
        mycursor.close()
        mydb.close()

# log currently logged in person out
@app.route('/logout', methods=['PUT'])
def logout():
    # Clear the user's session data
    session.clear()
    return jsonify({'status':'success'})


# Fetch student details
@app.route('/getstudents', methods=['GET'])
def get_students():
    try:
        if not (session['username'] == 'root@root.com'):
            return jsonify({'message': 'Student record not updated','exception':  'No rights to view student details','status' : 'failed'})
    except:
         return jsonify({'message': 'Student record not updated','exception':  'No rights to view student details','status' : 'failed'})
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
        mycursor.execute("SELECT * FROM student")
        students = mycursor.fetchall()
        studentsJson = []
        if students:
            for student in students:
                studentJson = {'studentId': student[0], 'fName': student[1], 'lName ':student[2], 'graduationYear':student[3],'email': student[4],'certNo': student[6],'role': student[7],'number': student[8]}
                studentsJson.append(studentJson)
            return jsonify({'students':studentsJson,'status':'success'}), 200
        else:
            return jsonify({'message': 'students not found. oh no','status':'failed'}), 404
    except Exception as e:
        return jsonify({'message': 'Student record not fetched','exception':  str(e),'status':'failed'}), 500
    finally:
        mycursor.close()
        mydb.close()


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)