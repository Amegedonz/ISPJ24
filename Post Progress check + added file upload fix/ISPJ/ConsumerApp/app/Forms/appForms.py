from DBcreateTables import User, Doctor
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (
    StringField, TextAreaField, PasswordField, IntegerField, 
    EmailField, SelectField, BooleanField, RadioField, FileField, SubmitField
)
from wtforms import validators 
from wtforms.validators import DataRequired, Length, Email, ValidationError
from email_validator import validate_email as ev, EmailNotValidError
import re
import bleach
from bleach.sanitizer import Cleaner


class LoginForm(FlaskForm):
    id = StringField("NRIC: ", [validators.InputRequired(), validators.Regexp(r'^[A-Za-z][0-9]{7}[A-Za-z]$', message = "please ensure correct NRIC")])
    password = PasswordField("Password: ",[validators.InputRequired()])
    remember = BooleanField("Remember me:", default= True )

class RegistrationForm(FlaskForm):
    name = StringField("* Name (As Per NRIC):  ",[validators.InputRequired()])
    id = StringField("* NRIC: " ,[validators.InputRequired(), validators.Regexp(r'^[A-Za-z][0-9]{7}[A-Za-z]$', message = "please ensure correct NRIC")])
    email = EmailField('Email:', [validators.Email(), validators.Optional()])
    phoneNumber = IntegerField('Phone Number:', [validators.NumberRange(6000000, 99999999), validators.Optional()])
    password = PasswordField('* Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number")])
    confirm = PasswordField('* Repeat Password:',[validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])

class TwoFactorForm(FlaskForm):
    otp = StringField('* Enter OTP' ,[validators.InputRequired(), validators.Length(min=6, max=6)])



# KENZIE
# Custom validator function to ensure only alphabetic characters and spaces are allowed for name
def validate_name(form, field):
    if not re.match("^[A-Za-z ]+$", field.data):  # Allow alphabetic characters and spaces
        raise ValidationError('Name must contain only alphabetic characters and spaces.')

# Custom validator function to ensure the email contains only allowed characters for Gmail
def validate_email(form, field):
    try:
        # Validate and canonicalize the email
        valid = ev(field.data)
        field.data = valid.email  # Replace with the canonicalized form
    except EmailNotValidError as e:
        raise ValidationError(str(e))

class CreateMessageForm(FlaskForm):
    name = StringField('Name', [
        validators.Length(min=1, max=150),
        validators.DataRequired(),
        validate_name
    ])
    email = EmailField('Email', [
        validators.Email(),
        validators.DataRequired(),
        validate_email
    ])
    message = TextAreaField('Message', [validators.DataRequired()])
    screenshot = FileField('Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Allowed file types are png, jpg, jpeg, gif')
    ])
    consent = BooleanField('I consent to the Data Privacy Terms', validators=[validators.DataRequired(message="You must agree to the data privacy terms before submitting.")])
    submit = SubmitField("Submit")