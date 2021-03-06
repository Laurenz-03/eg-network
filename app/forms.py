from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Benutzername:',
                           validators=[DataRequired(), Length(min=3, message='Der Benutzername muss mindestens drei Zeichen enthalten.'), Length(max=25, message='Der Benutzername darf nicht mehr als 25 Zeichen enthalten.')])

    email = StringField('eMail:',
                        validators=[DataRequired()])

    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=8, message='Das Passwort muss mindestens acht Zeichen enthalten.'), Length(max=60, message='Das Passwort darf nicht mehr als 60 Zeichen enthalten.')])

    confirm_password = PasswordField('Password bestätigen:',
                                     validators=[DataRequired(), EqualTo('password', message='Die Passwörter stimmen nicht überein.')])

    submit = SubmitField('Registrieren')

    # Testet, ob der Benutzername bereits in der Datenbank vorhanden ist
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.replace(" ", "")).first()
        if user:
            raise ValidationError('Dieser Benutzername ist bereits vergeben.')

    # Testet, ob die Email-Adresse bereits in der Datenbank vorhanden ist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.replace(" ", "")).first()
        if user:
            raise ValidationError('Diese Email-Adresse ist bereits vergeben.')

class LoginForm(FlaskForm):
    email_username = StringField('Email oder Benutzername:',
                        validators=[DataRequired()])

    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=8, message='Das Passwort muss mindestens acht Zeichen enthalten.'), Length(max=60, message='Das Passwort darf nicht mehr als 60 Zeichen enthalten.')])

    remember = BooleanField('Eingeloggt bleiben')

    submit = SubmitField('Einloggen')

class ChangeUsername(FlaskForm):
    username = StringField('Benutzername:',
                           validators=[Length(min=3, message='Der Benutzername muss mindestens drei Zeichen enthalten.'), Length(max=25, message='Der Benutzername darf nicht mehr als 25 Zeichen enthalten.')])

    submit = SubmitField('Speichern')

    # Testet, ob der Benutzername bereits in der Datenbank vorhanden ist
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Dieser Benutzername ist bereits vergeben.')

class ChangePassword(FlaskForm):
    password = PasswordField('Altes Passwort:',
                             validators=[DataRequired(), Length(min=8, message='Das Passwort muss mindestens acht Zeichen enthalten.'), Length(max=60, message='Das Passwort darf nicht mehr als 60 Zeichen enthalten.')])
    
    new_password = PasswordField('Neues Passwort:',
                             validators=[DataRequired(), Length(min=8, message='Das Passwort muss mindestens acht Zeichen enthalten.'), Length(max=60, message='Das Passwort darf nicht mehr als 60 Zeichen enthalten.')])

    confirm_new_password = PasswordField('Neues Passwort bestätigen:',
                                     validators=[DataRequired(), EqualTo('new_password', message='Die Passwörter stimmen nicht überein.')])

    submit = SubmitField('Speichern')

class RequestResetForm(FlaskForm):
    email = StringField('Email:',
                        validators=[DataRequired()])
    submit = SubmitField('Passwort zurücksetzen')

    # Testet, ob die Email-Adresse bereits in der Datenbank vorhanden ist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user is None:
            raise ValidationError('Es existiert kein Account mit dieser Email-Adresse.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password:',
                             validators=[DataRequired(), Length(min=8, message='Das Passwort muss mindestens acht Zeichen enthalten.'), Length(max=60, message='Das Passwort darf nicht mehr als 60 Zeichen enthalten.')])

    confirm_password = PasswordField('Password bestätigen:',
                                     validators=[DataRequired(), EqualTo('password', message='Die Passwörter stimmen nicht überein.')])

    submit = SubmitField('Passwort zurücksetzen')
    
class AddInstaAccForm(FlaskForm):
    instaname = StringField('Instagram Benutzername:',
                        validators=[DataRequired(), Length(max=60)])

    submit = SubmitField('Bestätigen')

class AdminChangeUserAcc(FlaskForm):
    username = StringField('Benutzername:')

    email = StringField('eMail:')
    email_confirmed = StringField('eMail confirmed:')

    rang = StringField('Rang:')
    
    eg_level = StringField('EG-Level:')

    instaname1 = StringField('Insta Name 1:')
    instaname2 = StringField('Insta Name 2:')
    instaname3 = StringField('Insta Name 3:')

    submit = SubmitField('Bestätigen')

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

class AnalyzerForm(FlaskForm):
    instaname = StringField('Instagram Benutzername:',
                        validators=[DataRequired(), Length(max=60, message='Das Benutzername darf nicht mehr als 60 Zeichen enthalten.')])

    submit = SubmitField('Analysieren')

class SendConfirmEmailForm(FlaskForm):

    submit = SubmitField('Email senden')

class ActivateProductForm(FlaskForm):
    product_key = StringField('Product Key:',
                        validators=[DataRequired()])

    submit = SubmitField('Aktivieren')

class SetPremiumForm(FlaskForm):
    user_id = StringField('User ID:', validators=[DataRequired()])
    days = StringField('Days:', validators=[DataRequired()])

    submit = SubmitField('Bestätigen')