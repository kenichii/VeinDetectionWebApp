from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'veindetection'

mysql = MySQL(app)


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = ""
        db = "veindetection"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_of_patients(self):
        self.cur.execute("SELECT * from patients_data_table")
        result = self.cur.fetchall()
        return result


@app.route('/')
def myApp():
    def db_query():
        db = Database()
        patients = db.list_of_patients()
        return patients

    res = db_query()
    return render_template('PatientsDataTable.html', result=res, content_type='application/json')

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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients_data_table "
                    "(patientid, firstname, lastname, middlename, phonenumber, address, city, municipality, zipcode, nationality, civilstatus, email, birthdate, birthplace) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                        patientid, firstname, lastname, middlename, phonenumber, address, city, municipality, zipcode,
                        nationality, civilstatus, email, birthdate, birthplace))
        mysql.connection.commit()
        return redirect(url_for('myApp'))

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
        cur = mysql.connection.cursor()
        cur.execute("""
                   UPDATE patients_data_table
                   SET patientid=%s, firstname=%s, lastname=%s, middlename=%s, phonenumber=%s, address=%s, city=%s, municipality=%s, zipcode=%s, nationality=%s, civilstatus=%s, email=%s, birthdate=%s, birthplace=%s
                   WHERE id=%s
                """, (
        patientid, firstname, lastname, middlename, phonenumber, address, city, municipality, zipcode, nationality,
        civilstatus, email, birthdate, birthplace, id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('myApp'))

@app.route('/delete/<string:id>', methods = ['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patients_data_table WHERE id=%s", (id,))
    mysql.connection.commit()
    flash("Record Has Been Deleted Successfully")
    return redirect(url_for('myApp'))