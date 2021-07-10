
import MySQLdb
from flask import Flask, render_template, request, session
# from MySQLdb import mysql
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "session"
# app.config["MYSSQL_S"]

mysql = MySQL(app)


@app.route('/', methods=["GET", "POST"])
def home_login():
    return render_template('login.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        ldetails = request.form
        email = ldetails["email"]
        password = ldetails["password"]
        # print("login : ", email, password)

        # select by login details
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE email = % s AND password = % s', (email, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return redirect('/home')
        else:
            return redirect ('/login')
    return render_template('login.html')


@app.route('/home',methods=["GET", "POST"])
def home():
    # try:
        if session.get("email"):
            cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor1.execute('SELECT * FROM desci WHERE name= % s AND uid = % s',(session['email'], session['id']))
            account1 = cursor1.fetchall()
            return render_template('home.html', sessi=session["email"], datass=account1, datas=account1)
        else:
            return redirect('/login')
    # except KeyError:
    #     return redirect('/login')
@app.route('/register')
def home_register():
    return render_template('register.html')

@app.route('/register_details', methods=["GET", "POST"])
def detail_register():
    if(request.method == "POST"):
        details = request.form
        email = details["email"]
        password = details["password"]
        cpassword = details["cpassword"]
        description = details["desc"]

        if(password == cpassword):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(email,password,description) VALUES (%s,%s,%s)",
                        (email, password, description))
            mysql.connection.commit()
            cur.close()
        else:
            return "plz checek"
    return render_template('login.html')


@app.route('/user_insert', methods=["GET", "POST"])
def user_insert():
    if(request.method == "POST"):
        insert_data = request.form
        item = insert_data["uinsert"]

        print("my session  : ",session["email"])
        print(item, session["id"])
        cur = mysql.connection.cursor()
        
        cur.execute("INSERT INTO `desci` (`name`, `desc`, `uid`) VALUES (%s,%s,%s)",(session['email'], item, session['id']))
        mysql.connection.commit()

        cur.execute('SELECT * FROM users WHERE email like %s',[session["email"]])
        account = cur.fetchone()

        cur.execute('SELECT * FROM desci WHERE uid = %s',[session['id']])
        acc = cur.fetchall()
        cur.close()
        print(acc,"\n")
    return redirect('/home')

@app.route('/logout')
def logout():  
    session.pop('loggedin', False)
    session.pop('id',None)
    session.pop('email',None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
