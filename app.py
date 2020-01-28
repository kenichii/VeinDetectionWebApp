from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
import pymysql
import MySQLdb.cursors
import os

from werkzeug.utils import secure_filename

from base64 import b64encode

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'veindetection'
mysql = MySQL(app)
patientids = ''


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = ""
        db = "veindetection"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def convertToBinaryData(filename):
        # Convert digital data to binary format
        with open(filename, 'wb') as file:
            binaryData = file.read()
        return binaryData

    def list_of_patients(self):
        self.cur.execute("SELECT * from patients_data_table")
        result = self.cur.fetchall()

        for row in result:
            row['veinimage'] = b64encode(row['veinimage']).decode("utf-8")
        return result

    def patient_info(self):
        self.cur.execute("SELECT * FROM patients_data_table WHERE id=%s", (patientids))
        result = self.cur.fetchall()

        for row in result:
            row['veinimage'] = b64encode(row['veinimage']).decode("utf-8")
        return result


@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('LoginForm.html', msg=msg)


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # API Call
        def db_query():
            db = Database()
            patients = db.list_of_patients()
            return patients

        res = db_query()
        return render_template('PatientsDataTable.html', result=res, content_type='application/json')

    # User is not loggedin redirect to login page
    return redirect('login')


app.config['IMAGE_UPLOADS'] = "C:/Users/Kenichi/PycharmProjects/VainDetectionWeb/static/img/uploads"
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ["PNG", "JPG", "JPEG", "GIF"]


def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        patientid = request.form['patientid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        middlename = request.form['middlename']
        phonenumber = request.form['phonenumber']
        address = request.form['address']
        city = request.form['city']
        municipality = request.form['municipality']
        zipcode = request.form['zipcode']
        nationality = request.form['nationality']
        civilstatus = request.form['civilstatus']
        email = request.form['email']
        birthdate = request.form['birthdate']
        birthplace = request.form['birthplace']
        file = request.files['file']
        filename = file.filename
        ext = file.filename.rsplit(".", 1)[1]

        file.save(os.path.join(app.config['IMAGE_UPLOADS'], file.filename))

        photo = convertToBinaryData(
            "C:/Users/Kenichi/PycharmProjects/VainDetectionWeb/static/img/uploads/" + file.filename)
        print(photo)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients_data_table "
                    "(patientid, firstname, lastname, middlename, phonenumber, address, city, municipality, zipcode, nationality, civilstatus, email, birthdate, birthplace, filename, veinimage) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                        patientid, firstname, lastname, middlename, phonenumber, address, city, municipality, zipcode,
                        nationality, civilstatus, email, birthdate, birthplace, filename, photo))
        mysql.connection.commit()
        return redirect(url_for('home'))


@app.route('/update', methods=['POST', 'GET'])
def updateData():
    if request.method == 'POST':
        id = request.form['id']
        patientid = request.form['patientid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        middlename = request.form['middlename']
        phonenumber = request.form['phonenumber']
        address = request.form['address']
        city = request.form['city']
        municipality = request.form['municipality']
        zipcode = request.form['zipcode']
        nationality = request.form['nationality']
        civilstatus = request.form['civilstatus']
        email = request.form['email']
        birthdate = request.form['birthdate']
        birthplace = request.form['birthplace']
        file = request.files['file']
        cur = mysql.connection.cursor()

        if file != '':
            file.save(os.path.join(app.config['IMAGE_UPLOADS'], file.filename))

            photo = convertToBinaryData(
                "C:/Users/Kenichi/PycharmProjects/VainDetectionWeb/static/img/uploads/" + file.filename)

            cur.execute("""
                               UPDATE patients_data_table
                               SET patientid=%s, firstname=%s, lastname=%s, middlename=%s, phonenumber=%s, address=%s, city=%s, municipality=%s, zipcode=%s, nationality=%s, civilstatus=%s, email=%s, birthdate=%s, birthplace=%s, filename=%s, veinimage=%s
                               WHERE id=%s
                            """, (
                patientid, firstname, lastname, middlename, phonenumber, address, city, municipality, zipcode,
                nationality,
                civilstatus, email, birthdate, birthplace, file.filename, photo, id))
        else:
            cur.execute("""
                               UPDATE patients_data_table
                               SET patientid=%s, firstname=%s, lastname=%s, middlename=%s, phonenumber=%s, address=%s, city=%s, municipality=%s, zipcode=%s, nationality=%s, civilstatus=%s, email=%s, birthdate=%s, birthplace=%s
                               WHERE id=%s
                            """, (
                patientid, firstname, lastname, middlename, phonenumber, address, city, municipality, zipcode,
                nationality,
                civilstatus, email, birthdate, birthplace, id))

        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('home'))


@app.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patients_data_table WHERE id=%s", (id,))
    mysql.connection.commit()
    flash("Record Has Been Deleted Successfully")
    """ try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()"""
    return redirect(url_for('home'))


@app.route('/profileinformation/<patientid>')
def profileInfo(patientid):
    global patientids
    patientids = patientid

    def db_query():
        db = Database()
        patients = db.patient_info()
        return patients

    res = db_query()
    """def get_profile_info():
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM patients_data_table WHERE id=%s', (patientid))
        result = cur.fetchone()
        return result"""

    return render_template('ProfileInformation.html', result=res, content_type='application/json')
