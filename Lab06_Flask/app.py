from flask import Flask, render_template, request
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     password = db.Column(db.String(80))
#     failed_attempts = db.Column(db.Integer, default=0)

#     def __init__(self, username, password):
#         self.username = username
#         self.password = bcrypt.generate_password_hash(password).decode('utf-8')

# def create_tables():
#     with app.app_context():
#         db.create_all()

@app.route("/")
def base():
    return render_template("base.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/password_check", methods=['POST'])
def password_check():
    #username = request.form['username']
    password = request.form['password']
    #user = User.query.filter_by(username=username).first()

    # if user:
    #     if bcrypt.check_password_hash(user.password, password):
    #         user.failed_attempts = 0
    #         db.session.commit()
    #     else:
    #         user.failed_attempts += 1
    #         db.session.commit()
    #         if user.failed_attempts >= 3:
    #             warning = 'Warning: Exceeded consecutive failed attempts limit'
    #             return render_template('index.html', warning=warning)
    #         else:
    #             warning = 'Incorrect password'
    #             return render_template('index.html', warning=warning)
    # else:
    requirements = {
        '8 characters': len(password) >= 8,
        'Atleast one uppercase letter': any(char.isupper() for char in password),
        'Atleast one lowercase letter': any(char.islower() for char in password),
        'Must end with a number': password[-1].isdigit()
    }

    failed_requirements = [requirement for requirement, passed in requirements.items() if not passed]

        # if len(failed_requirements) == 0:
        #     user = User(username, password)
        #     db.session.add(user)
        #     db.session.commit()

    return render_template('report.html', failed_requirements=failed_requirements or [])


if __name__ == '__main__':
    #create_tables()
    app.run(debug=True)
