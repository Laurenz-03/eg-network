from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Benutzername:',
                           validators=[DataRequired(), Length(min=3, message='Der Benutzername muss mindestens drei Zeichen enthalten.'), Length(max=25, message='Der Benutzername darf nicht mehr als 25 Zeichen enthalten.')])

    email = StringField('eMail:',
                        validators=[DataRequired(), Email(message='Ungültige Email-Adresse.')])

    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=8, message='Das Passwort muss mindestens acht Zeichen enthalten.'), Length(max=60, message='Das Passwort darf nicht mehr als 60 Zeichen enthalten.')])

    confirm_password = PasswordField('Password bestätigen:',
                                     validators=[DataRequired(), EqualTo('password', message='Die Passwörter stimmen nicht überein.')])

    submit = SubmitField('Registrieren')

    # Testet, ob der Benutzername bereits in der Datenbank vorhanden ist
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Dieser Benutzername ist bereits vergeben.')

    # Testet, ob die Email-Adresse bereits in der Datenbank vorhanden ist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Diese Email-Adresse ist bereits vergeben.')


class LoginForm(FlaskForm):
    email_username = StringField('Email oder Benutzername:',
                        validators=[DataRequired()])

    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=8, message='Das Passwort muss mindestens acht Zeichen enthalten.'), Length(max=60, message='Das Passwort darf nicht mehr als 60 Zeichen enthalten.')])

    remember = BooleanField('Eingeloggt bleiben')

    submit = SubmitField('Einloggen')
