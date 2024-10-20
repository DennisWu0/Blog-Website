from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SECRET_KEY'] =  'SECRET_KEY'
# initialize the database
db = SQLAlchemy(app)

# Create a db class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
 
    def __repr__(self):
        return f"<User {self.name}>"

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/form/add', methods=['GET', 'POST'])
def user_add():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('User already exists, please change your email')
            
        else:
            user = User(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User added successfully')
    users = User.query.order_by(User.date.asc()).all()
    return render_template('user_add.html',
                           form=form,
                           name=name,
                           users=users)


@app.route('/')
def index():
    first_name = "Dennis Wu 99, i'm super cool"
    safe_test = "Safe test every thing is Safe"
    cars = ["BMW", "Audi", "Benz", "Toyota",40708]
    return render_template('index.html', 
                           fn=first_name,
                           st=safe_test,
                           cars=cars)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# Create an error page
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/form', methods=['GET', 'POST'])
def form():
    name = None
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully')

    return render_template('form.html', 
                           form=form, 
                           name=name)

if __name__ == '__main__':
    app.run(debug=True)

#they use a lot the safe and striptags.
# title for capitalizing the first letter of the string