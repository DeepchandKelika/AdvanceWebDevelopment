from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os, re

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable = False)
    lastName = db.Column(db.String(20), nullable = False)
    emailAddress = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(80), nullable = False)
    failed_attempts = db.Column(db.Integer, default=0)

    def __init__(self,firstName, lastName, emailAddress, password):
        self.firstName = firstName
        self.lastName = lastName
        self.emailAddress = emailAddress
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

def create_tables():
    with app.app_context():
        db.create_all()

@app.route("/")
def base():
    warning = request.args.get('warning')
    failed_requirements = request.args.getlist('failed_requirements')

    return render_template("register.html",warning = warning, failed_requirements = failed_requirements)




@app.route("/accountValidate", methods = ['POST'])
def accountValidate():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    emailAddress = request.form['emailAddress']
    
    pattern = "[A-Za-z0-9._%+-]+@(?:gmail.com|uab.edu)$"
    if not re.match(pattern, emailAddress):
        warning = 'Invalid Email Address'
        return redirect(url_for('base', warning=warning))


    password = request.form['password']
    confirm_password = request.form['confirmPassword']

    requirements = {
            '8 characters': len(password) >= 8,
            'Atleast one uppercase letter': any(char.isupper() for char in password),
            'Atleast one lowercase letter': any(char.islower() for char in password),
            'Must end with a number': password[-1].isdigit()
        }

    failed_requirements = [requirement for requirement, passed in requirements.items() if not passed]

    if len(failed_requirements) == 0:
        if(password != confirm_password):
            warning = 'Password and ConfirmPassword do not match'
            return redirect(url_for('base', warning=warning))
    else:
        return redirect(url_for('base', failed_requirements=failed_requirements or []))

    
    
    try:
        user = User(firstName, lastName, emailAddress, password)
        db.session.add(user)
        db.session.commit()
        return render_template('thankyou.html')
    except IntegrityError as e:
        warning = 'Given email address is already being used'
        return redirect(url_for('base', warning=warning))


@app.route("/loginVerify", methods = ['POST'])
def loginVerify():
    email = request.form['emailAddress']
    password = request.form['password']

    user = User.query.filter_by(emailAddress = email).first()

    if user:
        if bcrypt.check_password_hash(user.password, password):
            user.failed_attempts = 0
            db.session.commit()
            return render_template('secretPage.html')
        else:
            user.failed_attempts += 1
            db.session.commit()
            if user.failed_attempts >= 3:
                warning = 'Warning: Exceeded consecutive failed attempts limit'
                return redirect(url_for('userLogin', warning=warning))
            else:
                warning = 'Incorrect password'
                return redirect(url_for('userLogin', warning=warning))

@app.route('/userLogin')
def userLogin(warning = None):
    
    return render_template('login.html', warning = warning)





if __name__ == '__main__':
    create_tables()
    app.run(debug=True)