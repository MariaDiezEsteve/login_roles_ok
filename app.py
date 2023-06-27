from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)
import config
import mysql.connector

app.config['SECRET_KEY'] = config.HEX_SEC_KEY
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['MYSQL_PORT'] = config.MYSQL_PORT

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['Email']
    password = request.form['Password']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE Email = %s AND Password = %s", (email, password))
    user = cur.fetchone()
    cur.close()

    if user is not None:
        session['logueado'] = True
        session['id'] = user[0]
        session['rol'] = user[1]

        if session['rol'] == "admin":
                return render_template("admin.html")
        elif session['rol'] == "usuario":
                return render_template("user.html")
    else:
        return render_template('index.html', message="Las credenciales no son correctas")
    

if __name__ == '__main__':
    app.run(debug=True)