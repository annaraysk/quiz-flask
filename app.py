from flask import Flask, render_template, url_for, request
import os
from hashlib import sha512
import sqlite3
import smtplib
from werkzeug.utils import redirect
from random import randint
from datetime import datetime

app = Flask(__name__)

isLoggedIn = False
username = 'Guest'
usergmail = ''
l=[106, 117, 115, 116, 83, 111, 109, 101, 83, 105, 109, 112, 108, 101, 83, 104, 105, 116]
ql=[]

@app.route('/')
@app.route('/index.html')
def index():
    global isLoggedIn
    global username
    return render_template("index.html", loggedin= isLoggedIn, user=username)

@app.route('/login.html')
def login():
    return render_template('login.html',msg='')

@app.route('/registration.html')
def registration():
    return render_template('registration.html', loggedin= isLoggedIn, user=username)

@app.route('/questions.html')
def questions():
    return render_template('questions.html')

@app.route('/quiz.html')
def quiz():
    return render_template('quiz.html', loggedin= isLoggedIn, user=username)

@app.route('/reset password.html')
def reset():
    return render_template('reset password.html',msg='')

@app.route('/about-us.html')
def about():
    return render_template('about-us.html', loggedin= isLoggedIn, user=username)

@app.route('/contact-us.html')
def contact():
    return render_template('contact-us.html', loggedin= isLoggedIn, user=username, msg='')

@app.route('/features.html')
def features():
    return render_template('features.html', loggedin= isLoggedIn, user=username)

@app.route('/forgot password.html')
def forgot():
    return render_template('forgot password.html')

@app.route('/profile.html')
def profile():
    global usergmail
    global username
    con = sqlite3.connect('creds.db')
    c = con.cursor()
    c.execute('select * from credstable where uname="'+str(usergmail)+'";')
    dat = c.fetchall()
    fname = dat[0][3]
    level = dat[0][2]
    tqs = dat[0][4]
    tqsc = dat[0][5]
    perc=(tqsc%10)*10
    return render_template('/profile.html',fname=fname, email=usergmail ,loggedin= isLoggedIn, user=username, level=level, tqs=tqs,tqsc=tqsc,tqsw=tqs-tqsc,perc=perc)

@app.route('/login', methods=['POST'])
def login_process():
    uname = request.form['email']
    password = request.form['entry']
    con = sqlite3.connect('creds.db')
    c = con.cursor()
    c.execute('select * from credstable where uname="'+str(uname)+'" and password="'+sha512(str(password).encode()).hexdigest()+'";')
    dat = c.fetchall()
    con.close()
    print(dat)
    if dat==[]:
        return render_template('/login.html',msg='fail')
    else:
        global isLoggedIn
        isLoggedIn = True
        global username
        username=dat[0][3].split()[0]
        global usergmail
        usergmail = dat[0][0]
        return redirect(url_for('index'))
    

@app.route('/register', methods=['POST'])
def reg_process():
    fname = request.form['fullName']
    p1 = request.form['passw']
    p2 = request.form['conpassw']
    if p1!=p2:
        return render_template('/registration.html',msg='pdm', loggedin= isLoggedIn, user=username) #pdm : password doesnt match
    em = request.form['email']
    con = sqlite3.connect('creds.db')
    c = con.cursor()
    c.execute('select * from credstable where uname="'+str(em)+'";')
    li = c.fetchall()
    if len(li)!=0:
        con.close()
        return render_template('/registration.html',msg='ear', loggedin= isLoggedIn, user=username) #ear : email already registered
    try:
        c.execute('insert into credstable values (?,?,?,?,?,?);',(str(em),sha512(p1.encode()).hexdigest(),0,fname,0,0))
        con.commit()
    except:
        con.close()
        return render_template('/registration.html',msg='sp', loggedin= isLoggedIn, user=username) #sp : server problem
    con.close()
    return render_template('/registration.html',msg='success', loggedin= isLoggedIn, user=username)

@app.route('/logout')
def logout():
    global isLoggedIn
    isLoggedIn = False
    global username
    username = 'Guest'
    return redirect(url_for('index'))

@app.route('/feedback',methods=['POST'])
def feedback():
    name= request.form['name']
    em = request.form['email']
    sub = request.form['sub']
    msg = request.form['msg']
    con = sqlite3.connect('creds.db')
    c= con.cursor()
    c.execute('insert into feedbacks values(?,?,?,?);' ,(name,em,sub,msg))
    con.commit()
    con.close()
    return render_template('/contact-us.html',loggedin= isLoggedIn, user=username, msg='success')

@app.route('/sendcode',methods=['POST'])
def sendcode():
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        otp=str(randint(100000,999999))
        smtp.login('qcorp.reset.code@gmail.com',''.join(list(map(chr,l))))
        subject = 'Reset Code for your QCorp Account'
        body = '''We recieved a password request for your QCorp Account\nThis code expires in 10 minutes.\nIf it was not you, You can safely ignore this email.
\n\nYour code is\n\n
        '''+str(otp)
        msg= f'Subject : {subject}\n\n{body}'
        smtp.sendmail('qcorp.reset.code@gmail.com',request.form['email'],msg)
    con = sqlite3.connect('creds.db')
    c = con.cursor()
    da = datetime.now()
    c.execute('insert into reset_code values(?,?,?); ',(request.form['email'],otp,da.hour*60+da.minute))
    con.commit()
    con.close()
    return redirect(url_for('reset'))

@app.route('/resetAction',methods=['POST'])
def resetAction():
    mail = request.form['email']
    code = request.form['code']
    ps = request.form['ps']
    cnps = request.form['cnps']
    if ps!=cnps:
        return render_template('/reset password.html',msg='psmm') #psmm : password mismatch
    con = sqlite3.connect('creds.db')
    c = con.cursor()
    c.execute('select * from reset_code where gmail="'+str(mail)+'" and otp='+str(code)+';')
    dat = c.fetchall()
    try:
        print(dat)
        print(dat[0][2],type(dat[0][2]))
    except:
        pass
    if dat==[]:
        return render_template('/reset password.html', msg='ic') #ic : invalid code
    exp = dat[-1][2]
    da = datetime.now()
    if (da.hour*60+da.minute-int(exp)>10):
        return render_template('/reset password.html',msg='ce') #ce : code expired
    c.execute('update credstable set password="'+sha512(ps.encode()).hexdigest()+'" where uname="'+mail+'";')
    con.commit()
    con.close()
    return render_template('/reset password.html',msg='success')
    
@app.route('/startquiz',methods=['POST'])
def startquiz():
    sub = request.form['subject']
    dif = request.form['diflevel']
    noq = request.form['noofqstns']
    global ql
    

if __name__=="__main__":
    app.run(debug=True)