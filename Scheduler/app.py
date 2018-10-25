from __future__ import print_function

import Database
import hashlib
import datetime
from twilio.rest import Client

from flask import Flask, render_template, session, request, url_for, redirect

app = Flask(__name__)
app.secret_key = 'abc123456'


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
        Database.db.cur.execute("""select * from users where username=:param1 and password=:param2""",
                                (username, password))
        data = Database.db.cur.fetchall()
        if Database.db.cur.rowcount > 0:
            session['username'] = data[0][0]
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid Username/Password!"
            return render_template('index.html', error=error)


@app.route('/create_account/')
def create_account():
    return render_template("create_account.html", form=None)


@app.route('/create_account/', methods=['POST'])
def add_user():
    if request.method == 'POST':

        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        zip = request.form['zip']
        email = request.form['email']
        username = request.form['username']

        password = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
        mobile1 = request.form['mobile1']
        mobile2 = request.form['mobile2']
        mobile3 = request.form['mobile3']

        if len(request.form['password']) < 8:
            error = "Password must be 8 characters long!"
            return render_template('create_account.html', error=error, form=request.form)
        else:
            Database.db.cur.execute("select username from users where username='" + username + "'")
            Database.db.cur.fetchall()
            if Database.db.cur.rowcount > 0:
                error = "Username already exists!"
                return render_template('create_account.html', error=error, form=request.form)
            else:

                Database.db.cur.execute("""insert into users values (:param1, :param2, :param3, :param4, :param5, :param6,  
                                        :param7, :param8, :param9, :param10,:param11,:param12,:param13)""",
                                        (username, fname, lname, gender, address1, address2, city, zip, email, password,mobile1,mobile2,mobile3))
                msg = "Data added successfully!"
                session['username'] = username
                return redirect(url_for('dashboard'))




@app.route('/dashboard/')
def dashboard():
    Database.db.cur.execute("select * from users where username='" + session['username'] + "'")

    groupID = Database.db.cur.fetchall()


    if Database.db.cur.rowcount > 0:
        Database.db.cur.execute(
            "select * from eventt where username='" + groupID[0][0] + "'")
        eventt = Database.db.cur.fetchall()
        edate = datetime.datetime.today()

        if Database.db.cur.rowcount <= 0:
            eventt = None
            rem=None
        else:
            i=0;
            j=Database.db.cur.rowcount;
            rem=None
            for i in range(0,j):
                s=eventt[i][3]

                s1 =datetime.datetime.strptime(s[:10], '%Y-%m-%d')

                if edate>=s1:

                    client = Client("ACc690b0318d276cecf5d6c66579e5420a", "1ef8de6f61798b301c85294fb02fdf5c")
                    a=groupID[0][10]
                    b='+91'+a
                    client.messages.create(to=b,
                                           from_="+17014019275",
                                           body="Event pending!\n"+eventt[i][1]+eventt[i][2])

                    a = groupID[0][11]
                    b = '+91' + a
                    client.messages.create(to=b,
                                           from_="+17014019275",
                                           body="Event pending!\n" + eventt[i][1] + eventt[i][2])

                    a = groupID[0][12]
                    b = '+91' + a
                    client.messages.create(to=b,
                                           from_="+17014019275",
                                           body="Event pending!\n" + eventt[i][1] + eventt[i][2])

                    """

                    client.messages.create(to="+919726308908",
                                           from_="+17014019275",
                                           body="Event pending!\n" + eventt[i][1] + eventt[i][2])
                    """
                    rem = None

        return render_template('dashboard.html', form=None, eventt=eventt,rem=rem)
    else:
        return redirect(url_for('index'))


@app.route('/add_event/')
def add_event():
    edate = datetime.datetime.today()
    return render_template("add_event.html", form=None, edate=edate)


@app.route('/add_event/', methods=['POST'])
def add_e():
    global ename, edate
    if request.method == 'POST':

        ename = request.form['projname']
        etime = request.form['etime']
        rtime = request.form['rtime']
        edate = datetime.datetime.today()

        a = session['username']
        Database.db.cur.execute("select * from users where username='" + a + "'")
        groupID = Database.db.cur.fetchall()
        if Database.db.cur.rowcount > 0:
            Database.db.cur.execute("""insert into eventt values(:param1, :param2, :param3, :param4, :param5)""",
                                    (groupID[0][0], ename, etime, rtime, 1))
            msg = "Data added successfully!"
            return render_template('add_event.html', msg=msg)
        else:
            msg = a
            return render_template('add_event.html', msg=msg)
        return redirect(url_for('add_event'))

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    Database.db.cur.close()
    Database.db.con.close()



"""DROP TABLE users;
DROP TABLE eventt;


CREATE TABLE users (username VARCHAR2(25) PRIMARY KEY, fname VARCHAR2(30), lname VARCHAR2(30), gender VARCHAR2(10), address1 VARCHAR2(200), address2 VARCHAR2(200), city VARCHAR2(50), zip VARCHAR2(10), email VARCHAR2(100), password VARCHAR2(50));
CREATE TABLE eventt (username VARCHAR2(25), enentname VARCHAR2(50), edate VARCHAR2(30), remdate VARCHAR2(30), status NUMBER(1));


"""