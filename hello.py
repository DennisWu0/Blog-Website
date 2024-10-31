from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
import re



app = Flask(__name__)
# add db
# the old db and now i want to connect to mysql db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/users_db'

# initialize the database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# secret key
app.config['SECRET_KEY'] =  'SECRET_KEY'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))



# Create a db class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    favorite_color = db.Column(db.String(80))
    
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f"<User {self.name}>"


# with app.app_context():
#     db.create_all()

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
    password_hash = PasswordField('Password', validators=[DataRequired()])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password_hash')])
    submit = SubmitField('Submit')


class PasswordForm(FlaskForm):
    email = StringField('What is your email?', validators=[DataRequired()])
    password_hash = PasswordField('What is your password?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/post/post_read/<int:id>', methods=['GET', 'POST'])
def read_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post_detail.html', post=post, id=id)


@app.route('/post')
def posts():
    
    posts = Post.query.order_by(Post.date.desc()).all()

    return render_template('post.html', posts=posts)


@app.route('/post_data', methods=['GET', 'POST'])
def post_data():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data,
            slug=form.slug.data
        )

        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()
        flash('Post added successfully')
    return render_template('post_data.html', form=form)

# edit page
@app.route('/post/post_edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.author = form.author.data
        post.slug = form.slug.data

        try:
            db.session.commit()
            flash('Post updated successfully')
            return redirect(url_for('posts'))
        except:
            flash('Error updating post')
            return redirect(url_for('posts'))
    else:
        form.title.data = post.title
        form.content.data = post.content
        form.author.data = post.author
        form.slug.data = post.slug
        return render_template('post_edit.html', form=form, post=post)

# delete page
@app.route('/post/post_delete/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Post deleted successfully')
        return redirect(url_for('posts'))
    except:
        flash('Error deleting post')
        return redirect(url_for('posts'))
    
    
    

# Create some Json here
@app.route('/date')
def date():
    aLotOfThing = {
        'first_name': "Dennis Wu 99, i'm super cool",
        'safe_test': "Safe test every thing is Safe",
        'cars': ["BMW", "Audi", "Benz", "Toyota", 40708]
        }

    return aLotOfThing


# Delete user
@app.route('/form/user_delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully')
        users = User.query.order_by(User.date.asc()).all()
        # return render_template('user_add.html',
        #                         form = form,
        #                         name = name,
        #                         users = users)
        return redirect(url_for('user_add'))
    except:
        flash("Error let's try again")
        # return render_template('user_add.html',
        #                         form = form,
        #                         name = name,
        #                         users = users)
        return redirect(url_for('user_add'))


# Update user form
@app.route('/form/user_update/<int:id>', methods=['GET', 'POST'])
def update(id):
    
    name_to_update = User.query.get_or_404(id)
    form = UserForm()
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try: 
            db.session.commit()
            flash('User updated successfully')
            return render_template('user_update.html', 
                                   form=form, 
                                   name_to_update=name_to_update)
        except:
            flash('Error man')
            return render_template('user_update.html', 
                                   form=form, 
                                   name_to_update=name_to_update)
    else: 
        return render_template('user_update.html', 
                               form=form, 
                               name_to_update=name_to_update,
                               id=id)


@app.route('/form/add', methods=['GET', 'POST'])
def user_add():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('User already exists, please change your email')
            
        else:
            hash_pw = generate_password_hash(form.password_hash.data)
            user = User(
                name=form.name.data, 
                email=form.email.data, 
                favorite_color=form.favorite_color.data,
                password_hash=hash_pw)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        # print(f"Stored hash: {user.password_hash}")  # Debug print
        # print(f"Password to check: {form.password_hash.data}")  # Debug print
        # print(check_password_hash(user.password_hash, form.password_hash.data))
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
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


@app.route('/pw_test', methods=['GET', 'POST'])
def pw_test():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        form.email.data = ''
        form.password_hash.data = ''
        # flash('Form submitted successfully')

        pw_to_check = User.query.filter_by(email=email).first()

        passed = check_password_hash(pw_to_check.password_hash, password)
        
    return render_template('pw_test.html', 
                           form=form, 
                           pw_to_check = pw_to_check,
                           email=email,
                           passed = passed,
                           password=password)


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