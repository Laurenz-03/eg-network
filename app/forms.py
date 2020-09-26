from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Benutzername:',
                           validators=[DataRequired(), Length(min=3, max=25)])

    email = StringField('eMail:',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=8, max=60)])

    confirm_password = PasswordField('Password bestätigen:',
                             validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Registrieren')

class LoginForm(FlaskForm):
    email = StringField('eMail:',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=8, max=60)])
    
    remember = BooleanField('Eingeloggt bleiben')

    submit = SubmitField('Registrieren')
