from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] =  'SECRET_KEY'

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


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