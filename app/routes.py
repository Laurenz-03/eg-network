from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, mail, admins, eg_boost_runden
from app.forms import RegistrationForm, LoginForm, ChangeUsername, ChangePassword, RequestResetForm, ResetPasswordForm, AddInstaAccForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import datetime
import pytz


# Startseite (Landing Page)
@app.route('/')
def landingPage():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    return render_template('pages/landingpage.html', title="Startseite", isLandingPage=True)

# Login und registrieren
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))

    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            register_form.password.data).decode('utf-8')
        user = User(username=register_form.username.data,
                    email=register_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(
            f'Account für {register_form.username.data} erfolgreich erstellt!', 'success')
        return redirect(url_for('mgb'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_by_email = User.query.filter_by(
            email=login_form.email_username.data).first()
        user_by_name = User.query.filter_by(
            username=login_form.email_username.data).first()
        next_page = request.args.get('next')
        print("success")
        if user_by_email and bcrypt.check_password_hash(user_by_email.password, login_form.password.data):
            login_user(user_by_email, remember=login_form.remember.data)
            flash('Du hast dich erfolgreich eingeloggt!', 'success')
            # Weiterleiten auf die Seite vor dem login
            return redirect(next_page) if next_page else redirect(url_for('mgb'))
        elif user_by_name and bcrypt.check_password_hash(user_by_name.password, login_form.password.data):
            login_user(user_by_name, remember=login_form.remember.data)
            flash('Du hast dich erfolgreich eingeloggt!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('mgb'))
        else:
            flash('Falsches Passwort oder falsche Email-Adresse.', 'no-success')
    return render_template('pages/login.html', title="Einloggen", register_form=register_form, login_form=login_form, nosidebar=True, nav_links_category='no-links')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = 'Um dein Passwort zurückzusetzen, klicke auf folgenden Link: ' + url_for('reset_token', token=token, _external=True)
    
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Die Email zum Zurücksetzen deines Passwortes wurde versendet.', 'success')
        return redirect(url_for('login'))
    return render_template('pages/reset_request.html', title="Passwort zurücksetzten", form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Der Link ist ungültig oder abgelaufen.', 'no-success')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        login_user(user)
        flash('Dein Passwort wurde aktualisiert!', 'success')
        return redirect(url_for('mgb'))
    return render_template('pages/reset_token.html', title="Passwort zurücksetzten", form=form)


@app.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsername()
    if form.validate_on_submit():
        user = current_user
        user.username = form.username.data
        db.session.commit()
        flash('Deine Änderungen wurden gespeichert!', 'success')
        return redirect(url_for('mgb'))
    return render_template('pages/change_username.html', title='Account bearbeiten', form=form)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        user = current_user
        if bcrypt.check_password_hash(user.password, form.password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Deine Änderungen wurden gespeichert!', 'success')
            return redirect(url_for('mgb'))
        else:
            flash('Das Passwort ist falsch.', 'no-success')
    return render_template('pages/change_password.html', title='Account bearbeiten', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landingPage'))


@app.route('/impressum')
def impressum():
    return render_template('pages/impressum.html', title="Impressum", nosidebar=True, nav_links_category='only-login')

# Alle Seiten im Mitgliederbereich
@app.route('/mgb')
@login_required
def mgb():
    return render_template('pages/mgb.html', title="Home", loginRequired=True)


@app.route('/mgb/egboost')
@login_required
def egboost():
    for runde in eg_boost_runden:

        # aktuelle Zeit und Datum
        date_now = datetime.datetime.utcnow()

        # time Objekte mit datetime Objekten zu neuen datetime Objekten kombinieren
        start_time = datetime.datetime.combine(date_now, runde["start-time"])
        upload_end_time = datetime.datetime.combine(
            date_now, runde["upload-end-time"])

        # Differenz berechnen (timedelta Objekt entsteht), die Sekunden durch 60 teilen um Minuten zu erhalten
        upload_anzMinutes = (upload_end_time - start_time).total_seconds() / 60

        upload_minutes_passed = (date_now - start_time).total_seconds() / 60
        # damit keine negative Zahl rauskommt
        upload_minutes_passed = 0 if upload_minutes_passed < 0 else upload_minutes_passed

        upload_time_factor = upload_minutes_passed / upload_anzMinutes * 100
        # damit der Faktor für die Progressbar nicht > 100 wird
        upload_time_factor = 100 if upload_time_factor > 100 else upload_time_factor

        # time Objekte mit datetime Objekten zu neuen datetime Objekten kombinieren
        engage_end_time = datetime.datetime.combine(
            date_now, runde["engage-end-time"])

        # Differenz berechnen (timedelta Objekt entsteht), die Sekunden durch 60 teilen um Minuten zu erhalten
        engage_anzMinutes = (engage_end_time - start_time).total_seconds() / 60

        engage_minutes_passed = (date_now - start_time).total_seconds() / 60
        # damit keine negative Zahl rauskommt
        engage_minutes_passed = 0 if engage_minutes_passed < 0 else engage_minutes_passed

        engage_time_factor = engage_minutes_passed / engage_anzMinutes * 100
        # damit der Faktor für die Progressbar nicht > 100 wird
        engage_time_factor = 100 if engage_time_factor > 100 else engage_time_factor

        # berechnen, wann die nächste Runde anfängt
        next_round_duration = start_time - date_now
        # print(next_round_duration)
        m, s = divmod(next_round_duration.total_seconds() + 60, 60)
        h, m = divmod(m, 60)
        h = h+24 if h < 0 else h

        runde['next-round-duration'] = [int(h), int(m)]
        runde['upload-time-factor'] = upload_time_factor
        runde['engage-time-factor'] = engage_time_factor
    return render_template('pages/egboost.html', title="EG-Boost", loginRequired=True, eg_boost_runden=eg_boost_runden, datetime=datetime)


@app.route('/mgb/tools')
@login_required
def tools():
    return render_template('pages/tools.html', title="Tools & Gruppen", loginRequired=True)


@app.route('/mgb/premium')
@login_required
def premium():
    return render_template('pages/premium.html', title="Premium", loginRequired=True)


@app.route('/mgb/hashtaggenerator')
@login_required
def hashtaggenerator():
    return render_template('pages/hashtaggenerator.html', title="Hashtag-Generator", loginRequired=True)


@app.route('/mgb/accountanalyse')
@login_required
def accountanalyse():
    return render_template('pages/accountanalyse.html', title="Account-Analyse", loginRequired=True)


@app.route('/mgb/shoutoutmatcher')
@login_required
def shoutoutmatcher():
    return render_template('pages/shoutoutmatcher.html', title="Shoutout-Matcher", loginRequired=True)


@app.route('/mgb/ebookskurse')
@login_required
def ebookskurse():
    return render_template('pages/ebookskurse.html', title="eBooks & Kurse", loginRequired=True)


@app.route('/mgb/profile')
@login_required
def profile():
    return render_template('pages/profile.html', title="Mein Profil", loginRequired=True)

@app.route('/add-insta-acc', methods=['GET', 'POST'])
@login_required
def add_insta_acc():
    if current_user.instaname1:
        flash('Du hast bereits einen Instagram Account hinzugefügt. Kaufe den Premium-Rang um bis zu drei Accounts hinzuzufügen.', 'success')
    else:
        form = AddInstaAccForm()
        if form.validate_on_submit():
            user = current_user
            user.instaname1 = form.instaname.data
            db.session.commit()
            return redirect(url_for('profile'))
            flash('Der Instagram Account wurde hinzugefügt!', 'success')
    return render_template('pages/add_insta_acc.html', title='Instagram Account verknüpfen', form=form)

# Nur für Admins
@app.route('/admin')
@login_required
def admin():
    # Man kommt nur auf die Admin Seite, wenn der Benutzername in der Liste der Admins steht
    if current_user.username in admins:
        users = User.query.all()
        # register_date=user.date_created.strftime('%d')
        return render_template('pages/admin.html', title="Admin-Dashboard", loginRequired=True, nosidebar=True, nav_links_category='only-login', users=users)
    else:
        flash('Du hast keine Admin Rechte. Haha.', 'no-success')
        return redirect(url_for('landingPage'))


@app.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    # Man kommt nur auf die Admin Seite, wenn der Benutzername in der Liste der Admins steht
    if current_user.username in admins:
        if user_id != 1:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
        else:
            flash(
                'Der Account von Laurenz dem Programmier-Gott kann nicht gelöscht werden.', 'no-success')
        return redirect(url_for('admin'))
    else:
        flash('Du hast keine Admin Rechte. Haha.', 'no-success')
        return redirect(url_for('landingPage'))
