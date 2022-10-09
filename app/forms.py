from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter username!')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password!')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Enter your name!')])
    email = StringField('Email', validators=(DataRequired(), Email(message='Invalid  email')))
    password = PasswordField('Password', validators=[DataRequired(message='Enter your password!')])
    password2 = PasswordField('Confirm Password', 
                validators=(DataRequired(message='Field required!'), EqualTo('password')))
    submit = SubmitField('Register')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Username already exists')
    #
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Email already exists.')

class QuestionForm(FlaskForm):
    options = RadioField('Options: ', validators=[DataRequired()])
    check = SubmitField('Check')
    submit = SubmitField('Next')