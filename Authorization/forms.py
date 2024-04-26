from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class NewUserForm(FlaskForm):
    first_name = StringField('First Name', 
                            validators = [InputRequired(), Length(max = 30)]) 
    last_name = StringField('Last Name', 
                            validators = [InputRequired(), Length(max = 30)])  
    username = StringField('Username', 
                           validators = [InputRequired(), Length(min = 1, max = 30)])
    password = PasswordField('Password', 
                            validators = [InputRequired(), Length(min = 6, max = 30)])
    email = StringField('Email', 
                            validators = [InputRequired(), Email(), Length(max = 50)])

class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators = [InputRequired(), Length(min = 1, max = 30)])
    password = PasswordField('Password', 
                            validators = [InputRequired(), Length(min = 6, max = 30)])
    

class FeedbackForm(FlaskForm):
    title = StringField('Title', 
                            validators = [InputRequired(), Length(max = 50)])
    content = StringField('Content', 
                            validators = [InputRequired()])
    
class DeleteForm(FlaskForm):
    """For security, rendering, and code maintainabilty purposes"""