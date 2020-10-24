from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, mail, admins, eg_boost_runden
from app.forms import RegistrationForm, LoginForm, ChangeUsername, ChangePassword, RequestResetForm, ResetPasswordForm, AddInstaAccForm, AdminChangeUserAcc
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import datetime
import pytz

import requests
import json


# Instagram API
def get_user_information_by_username(username):
    user_info = {}
    url = 'https://www.instagram.com/'+username+'/?__a=1'
    print(url)
    #url = 'https://www.instagram.com/{}/?__a=1'
    try:
        resp = requests.get(url=url).json()
        userdata = resp["graphql"]["user"]
        user_info["id"] = userdata["id"]
        user_info["username"] = username
        user_info["followers"] = userdata["edge_followed_by"]["count"]
        user_info["following"] = userdata["edge_follow"]["count"]
        user_info["profile_pic_url"] = userdata["profile_pic_url"]
    except:
        flash('Fehler 1', 'no-success')
        return redirect(url_for('admin'))
    return user_info

def get_user_by_id(user_id):
    user = {}
    if user_id:
        base_url = "https://i.instagram.com/api/v1/users/{}/info/"
        #valid user-agent
        headers = {
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
        }
        try:
            res       = requests.get(base_url.format(user_id),headers=headers)
            user_info = res.json()
            user      = user_info.get('user',{})["username"]
        except Exception as e:
            print("getting user failed, due to '{}'".format(e.message))
    return user

def calc_egboost_times():
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

@app.route('/test')
def api_test():
    resp = requests.get(url='https://api.coingecko.com/api/v3/coins/list').json()
    return str(resp)
@app.route('/')
def chooseLanguage():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    return render_template('pages/chooselanguage.html', nosidebar=True, nav_links_category='no-links')

# Startseite (Landing Page)
@app.route('/de')
def landingPageDE():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    return render_template('pages/landingpageDE.html', title="Startseite", isLandingPage=True, language='de')

@app.route('/en')
def landingPageEN():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    return render_template('pages/landingpageEN.html', title="Homepage", isLandingPage=True, language='en')

# Login und registrieren
def send_confirm_email(user):
    token = user.get_reset_token()
    msg = Message('Confirm Email', sender='noreply@eg-network.co', recipients=[user.email])
    #msg.html = render_template('./EG-Confirm/EG-Confirm-Email.html')
    msg.body = f'''Hallo {user.username},

um deine Email zu bestätigen, klicke auf folgenden Link:
{url_for("confirm_email", token=token, _external=True)}'''
    
    mail.send(msg)


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
        user = current_user
        send_confirm_email(user)
        flash(
            f'Wir haben dir eine Email an {user.email} gesendet. Bitte klicke auf den Link in der Email, um deinen Account zu bestätigen', 'info')
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
    msg = Message('Password Reset Request', sender='noreply@eg-network.co', recipients=[user.email])
    #msg.html = render_template('./EG-Passwort-Reset-Email/EG-Passwort-Reset-Email.html')
    msg.body = f'''Hallo {user.username},

um dein Passwort zurückzusetzen, klicke auf folgenden Link:
{url_for("reset_token", token=token, _external=True)}'''
    
    mail.send(msg)

@app.route('/confirm-email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('Der Link ist ungültig oder abgelaufen.', 'no-success')
        return redirect(url_for('login'))
    else:
        user.email_confirmed = 'true'
        db.session.commit()
        flash('Dein Account wurde bestätigt!', 'success')
        return redirect(url_for('mgb'))

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
    return redirect(url_for('chooseLanguage'))


@app.route('/impressum')
def impressum():
    return render_template('pages/impressum.html', title="Impressum", nosidebar=True, nav_links_category='only-login')


@app.route('/policies')
def policies():
    return render_template('pages/policies.html', title="Policies", nosidebar=True, nav_links_category='only-login')

# Alle Seiten im Mitgliederbereich
@app.route('/mgb')
@login_required
def mgb():
    calc_egboost_times()
    return render_template('pages/mgb.html', title="Home", loginRequired=True, eg_boost_runden=eg_boost_runden, datetime=datetime)


@app.route('/mgb/egboost')
@login_required
def egboost():
    calc_egboost_times()
    return render_template('pages/egboost.html', title="EG-Boost", loginRequired=True, eg_boost_runden=eg_boost_runden, datetime=datetime)


@app.route('/mgb/tools')
@login_required
def tools():
    return render_template('pages/tools.html', title="Tools & Gruppen", loginRequired=True)


@app.route('/mgb/telegramgroups')
@login_required
def telegramgroups():
    return render_template('pages/telegramgroups.html', title="Telegram Gruppen", loginRequired=True)


@app.route('/mgb/tutorials')
@login_required
def tutorials():
    return render_template('pages/tutorials.html', title="Tutorials", loginRequired=True)

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
    user = current_user
    insta_acc1_info = {}
    if user.instaid1:
        try:
            #insta_acc1_info = get_user_information_by_username('erfolgsarmee')
            #insta_acc1_info['username'] = get_user_by_id(user.instaid1)
            insta_acc1_info = get_user_information_by_username(get_user_by_id(user.instaid1))
        except:
            insta_acc1_info['username'] = "Fehler"
    return render_template('pages/profile.html', title="Mein Profil", loginRequired=True, insta_acc1_info=insta_acc1_info)

@app.route('/add-insta-acc', methods=['GET', 'POST'])
@login_required
def add_insta_acc():
    form = AddInstaAccForm()
    if current_user.instaid1:
        flash('Du hast bereits einen Instagram Account hinzugefügt. Kaufe den Premium-Rang um bis zu drei Accounts hinzuzufügen.', 'success')
        return redirect('mgb/profile')
    else:
        if form.validate_on_submit():
            user = current_user
            res = get_user_information_by_username(form.instaname.data)
            print('test:')
            print(res)
            user.instaid1 = res["id"]
            db.session.commit()
            return redirect(url_for('profile'))
            flash('Der Instagram Account wurde hinzugefügt!', 'success')
    return render_template('pages/add_insta_acc.html', title='Instagram Account verknüpfen', form=form)

@app.route('/del-insta-acc')
def del_insta_acc():
    user = current_user
    user.instaid1 = None
    db.session.commit()
    flash('Der Instagram Account wurde entfernt.', 'success')
    return redirect(url_for('profile'))

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
        return redirect(url_for('chooseLanguage'))


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
        return redirect(url_for('chooseLanguage'))

@app.route('/admin/change-user-details/<int:user_id>', methods=['GET', 'POST'])
def admin_change_user_details(user_id):
    user = User.query.get_or_404(user_id)
    # Man kommt nur auf die Admin Seite, wenn der Benutzername in der Liste der Admins steht
    if current_user.username in admins:
        form = AdminChangeUserAcc()
        if form.validate_on_submit():
            user.username = form.username.data if form.username.data else user.username
            user.email = form.email.data if form.email.data else user.email
            user.rang = form.rang.data if form.rang.data else user.rang
            user.eg_level = int(form.eg_level.data) if form.eg_level.data else user.eg_level
            user.instaid1 = int(form.instaname1.data) if form.instaname1.data else user.instaid1
            user.instaid2 = int(form.instaname2.data) if form.instaname2.data else user.instaid2
            user.instaid3 = int(form.instaname3.data) if form.instaname3.data else user.instaid3
            db.session.commit()
            flash('Deine Änderungen wurden gespeichert!', 'success')
            return redirect(url_for('admin'))
    else:
        flash('Du hast keine Admin Rechte. Haha.', 'no-success')
        return redirect(url_for('chooseLanguage'))
    flash('Leere Felder bewirken keine Änderung.', 'info')
    return render_template('pages/admin_change_user_details.html', title=f'Account von {user.username} bearbeiten', form=form, user=user)