"""Authentication forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models.team_members import TeamMember

class LoginForm(FlaskForm):
    """User login form."""
    email = StringField('Email', validators=[
        DataRequired(),
        Length(1, 120),
        Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    """User registration form."""
    member_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(1, 100)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Length(1, 120),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(8, 64, message='Password must be at least 8 characters long.')
    ])
    password2 = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        """Validate email is not already registered."""
        if TeamMember.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

class PasswordResetRequestForm(FlaskForm):
    """Form to request password reset."""
    email = StringField('Email', validators=[
        DataRequired(),
        Length(1, 120),
        Email()
    ])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    """Form to reset password."""
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(8, 64, message='Password must be at least 8 characters long.')
    ])
    password2 = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Reset Password')
