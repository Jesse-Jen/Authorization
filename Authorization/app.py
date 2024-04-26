from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import NewUserForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/', methods = ['GET'])
def redirect_homepage():
    '''redirects to homepage'''
    return redirect('/register')

@app.route('/', methods = ['GET', 'POST'])
def register():
    '''registers user and handles form submission'''

    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")
    else:
        return render_template('users/register.html', form = form)
    
@app.route('/login', methods = ['GET','POST'])
def login():
    '''shows login form and handles login'''
    if 'username' in session:
        return redirect(f"/users/{session['username']}")
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash('Welcome')
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid Username/Password']
            return render_template('/users/login.html', form = form)
        
    return render_template('/users/login.html', form = form)

@app.route('/logout', methods = ['GET'])
def logout():
    '''removing username from session'''
    session.pop('username')
    flash('Goodbye!')
    return redirect('/login')
       
@app.route("/users/<username>", methods = ['GET'])
def show_user_info(username):
    '''shows user info/feedback'''
    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", form = form, user = user)

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):
    '''deleting user'''
    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def add_feedback(username):
    '''show feedbackform and handles the submission'''
    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title = title, content = content, username = username)

        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    else: 
        return render_template('feedback/new.html', form = form)
    
@app.route('/feedback/<int:fid>/update', methods = ['GET', 'POST'])
def update_feedback(fid):
    '''show a form for feedback updates and handle submission'''

    feedback = Feedback.query.get(fid)
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()
    #filling out form with existing data
    form = FeedbackForm(obj = feedback)

    if form.validate_on_submit():
        feedback.title =  form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    
    return render_template('/feedback/edit.html', feedback = feedback, form = form)

@app.route('/feedback/<int:fid>/delete', methods = ['POST'])
def delete_feedback(fid):
    '''delete feedback'''
    feedback = Feedback.query.get(fid)
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()
    form = DeleteForm()
    
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f"/users/{feedback.username}")



