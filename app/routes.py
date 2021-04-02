from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, mail, admins, eg_boost_runden, zeitfaktor
from app.forms import (RegistrationForm, LoginForm, ChangeUsername, ChangePassword, RequestResetForm,
                       ResetPasswordForm, AddInstaAccForm, AdminChangeUserAcc, AnalyzerForm, SendConfirmEmailForm,
                       ActivateProductForm, SetPremiumForm)
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import datetime
import pytz

import requests
import json
import random


def create_session():
    cookie = {"name": "sessionid",
              "value": "7699609214%3A88flrRDxtPZREw%3A16"}
    session = requests.Session()
    session.cookies.set(**cookie)
    return session

# Instagram API


def get_user_information_by_username(username):
    user_info = {}
    url = 'https://www.instagram.com/'+username+'/?__a=1'
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
    }
    s = create_session()
    res = s.get(url=url, headers=headers)
    print("res:")
    resp = res.json()
    userdata = resp["graphql"]["user"]
    user_info["id"] = userdata["id"]
    user_info["username"] = username
    user_info["bio"] = userdata["biography"]
    user_info["followers"] = userdata["edge_followed_by"]["count"]
    user_info["following"] = userdata["edge_follow"]["count"]
    user_info["profile_pic_url"] = userdata["profile_pic_url"]
    return user_info


def get_user_by_id(user_id):
    s = create_session()
    user = {}
    if user_id:
        base_url = "https://i.instagram.com/api/v1/users/{}/info/"
        # valid user-agent
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
        }
        res = s.get(base_url.format(user_id), headers=headers)
        user_info = res.json()
        user = user_info.get('user', {})["username"]
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

def set_premium_end_date(id, days):
    user = User.query.get_or_404(id)
    end_time = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    print(user.username)
    print(end_time)

    user_info_json = json.loads(user.user_info)
    if "premium_end_date" in user_info_json:
        user_info_json["premium_end_date"] = str(end_time)
    else:
        user_info_json["premium_end_date"] = str(end_time)
    user.user_info = json.dumps(user_info_json)
    db.session.commit()

@app.route('/test')
def api_test():
    resp = requests.get(
        url='https://api.coingecko.com/api/v3/coins/list').json()
    return str(resp)


@app.route('/')
def chooseLanguage():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    return render_template('pages/chooselanguage.html', nosidebar=True, nav_links_category='no-links')

@app.route('/de/dailysuccess')
def landingPageDEDailysuccess():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    return render_template('pages/landingpageDE.html', title="Startseite", isLandingPage=True, language='de', aff_id="107")

# Startseite (Landing Page)
@app.route('/de')
def landingPageDE():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    return render_template('pages/landingpageDE.html', title="Startseite", isLandingPage=True, language='de', aff_id="1")


@app.route('/en')
def landingPageEN():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    return render_template('pages/landingpageEN.html', title="Homepage", isLandingPage=True, language='en')

# Login und registrieren


def send_confirm_email(user):
    token = user.get_reset_token()
    msg = Message('Confirm Email', sender='noreply@eg-network.co',
                  recipients=[user.email])
    link = url_for("confirm_email", token=token, _external=True)
    msg.html = render_template('pages/EG-Confirm-Email.html', link=link)
    mail.send(msg)


def email_confirm_required():
    if current_user.email_confirmed == 'false':
        send_confirm_email(current_user)
        flash(
            f'Um auf diese Funktion Zugriff zu erhalten, musst du deine Email-Adresse bestätigen. Wir haben dir eine Email an {current_user.email} gesendet. Bitte klicke auf den Link in der Email, um deinen Account zu bestätigen.', 'info')
        return redirect(url_for('mgb'))


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login_no_aff():
    return redirect(url_for('login', a="1"))


@app.route('/login/<a>', methods=['GET', 'POST'])
def login(a):
    affiliate_id = a
    print(a)
    if affiliate_id != None:
        try:
            aff_user = User.query.filter_by(id=affiliate_id).first()
            print(aff_user.username)

        except:
            affiliate_id = None
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))

    register_form = RegistrationForm()
    if register_form.validate_on_submit():

        # Affiliate Einladung verwalten
        aff_user_info_json = json.loads(aff_user.user_info)
        if "affiliate_invites" in aff_user_info_json:
            aff_user_info_json["affiliate_invites"] += 1
        else:
            aff_user_info_json["affiliate_invites"] = 1
        aff_user.user_info = json.dumps(aff_user_info_json)
        db.session.commit()
        print(aff_user.user_info)
        print(aff_user.username)

        hashed_password = bcrypt.generate_password_hash(
            register_form.password.data.strip()).decode('utf-8')
        user = User(username=register_form.username.data.strip(),
                    email=register_form.email.data.strip().lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(
            f'Account für {register_form.username.data} erfolgreich erstellt!', 'success')
        user = current_user
        send_confirm_email(user)
        flash(
            f'Wir haben dir eine Email an {user.email} gesendet. Bitte klicke auf den Link in der Email, um deinen Account zu bestätigen', 'info')
        return redirect(url_for('new_registered'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_by_email = User.query.filter_by(
            email=login_form.email_username.data.strip().lower()).first()
        user_by_name = User.query.filter_by(
            username=login_form.email_username.data.strip()).first()
        next_page = request.args.get('next')
        print("success")
        if user_by_email and bcrypt.check_password_hash(user_by_email.password, login_form.password.data.strip()):
            login_user(user_by_email, remember=login_form.remember.data)
            flash('Du hast dich erfolgreich eingeloggt!', 'success')
            # Weiterleiten auf die Seite vor dem login
            return redirect(next_page) if next_page else redirect(url_for('mgb'))
        elif user_by_name and bcrypt.check_password_hash(user_by_name.password, login_form.password.data.strip()):
            login_user(user_by_name, remember=login_form.remember.data)
            flash('Du hast dich erfolgreich eingeloggt!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('mgb'))
        else:
            flash('Falsches Passwort oder falsche Email-Adresse.', 'no-success')
    return render_template('pages/login.html', title="Einloggen", register_form=register_form, login_form=login_form, nosidebar=True, nav_links_category='no-links')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@eg-network.co', recipients=[user.email])
    link = url_for("reset_token", token=token, _external=True)
    msg.html = render_template('pages/EG-Passwort-Reset-Email.html', link=link)
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
        user = User.query.filter_by(
            email=form.email.data.strip().lower()).first()
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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
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
            hashed_password = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
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


@app.route('/email-not-confirmed', methods=['GET', 'POST'])
@login_required
def email_not_confirmed():
    if current_user.email_confirmed == 'false':
        flash(f'Um auf diese Funktion Zugriff zu erhalten, musst du deine Email-Adresse bestätigen.', 'info')
        form = SendConfirmEmailForm()
        if form.validate_on_submit():
            send_confirm_email(current_user)
            flash(
                f'Die Email zur Bestätigung deines Accounts wurde an {current_user.email} gesendet.', 'success')
            return redirect(url_for('mgb'))
    else:
        return redirect(url_for('mgb'))
    return render_template('pages/email_not_confirmed.html', title="Email bestätigen", form=form)


# Alle Seiten im Mitgliederbereich
@app.route('/mgb')
@login_required
def mgb():
    calc_egboost_times()

    # neue Zeit setzen
    current_time = str(datetime.datetime.utcnow())
    user_info_json = json.loads(current_user.user_info)
    user_info_json["last_online"] = current_time
    current_user.user_info = json.dumps(user_info_json)
    db.session.commit()

    return render_template('pages/mgb.html', title="Home", loginRequired=True, eg_boost_runden=eg_boost_runden, datetime=datetime)

@app.route('/mgb/new_registered')
@login_required
def new_registered():
    return render_template('pages/new_registered.html', title="Home", loginRequired=True)

@app.route('/mgb/egboost')
@login_required
def egboost():
    if current_user.email_confirmed == 'false':
        return redirect(url_for('email_not_confirmed'))

    if current_user.instaid1 == None:
        flash('Um an EG-Boost teilzunehmen, musst du erst deinen Instagram Account verknüpfen.', 'info')

    user_info_json = json.loads(current_user.user_info)
    if "acc_request_status" not in user_info_json:
        user_info_json["acc_request_status"] = {}
        current_user.user_info = json.dumps(user_info_json)
        db.session.commit()

    calc_egboost_times()

    user_info_json = json.loads(current_user.user_info)
    return render_template('pages/egboost.html', title="EG-Boost", loginRequired=True, eg_boost_runden=eg_boost_runden, user_info=user_info_json, datetime=datetime, zeitfaktor=zeitfaktor)


@app.route('/mgb/account_anfragen/<eg_acc_name>')
@login_required
def account_anfragen(eg_acc_name):
    instaname1 = get_user_by_id(current_user.instaid1)
    instaname2 = get_user_by_id(
        current_user.instaid2) if current_user.instaid2 else "None"
    instaname3 = get_user_by_id(
        current_user.instaid3) if current_user.instaid3 else "None"

    # öffnet die Datei mit der Anfragenliste
    with open('anfragenliste.json') as f:
        anfragenliste = json.load(f)

    if instaname1 not in anfragenliste[eg_acc_name]:
        anfragenliste[eg_acc_name].append(instaname1)
    if instaname2 not in anfragenliste[eg_acc_name] and instaname2 != "None":
        anfragenliste[eg_acc_name].append(instaname2)
    if instaname3 not in anfragenliste[eg_acc_name] and instaname3 != "None":
        anfragenliste[eg_acc_name].append(instaname3)

    with open('anfragenliste.json', 'w') as f:
        json.dump(anfragenliste, f)

    user_info_json = json.loads(current_user.user_info)
    if "acc_request_status" in user_info_json:
        print("yes")
    else:
        user_info_json["acc_request_status"] = {eg_acc_name: "pending"}

    user_info_json["acc_request_status"][eg_acc_name] = "pending"
    current_user.user_info = json.dumps(user_info_json)
    db.session.commit()
    print(user_info_json)
    flash("Anfrage wurde erfolgreich gesendet!", "success")
    return redirect(url_for('egboost'))


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
    premium_end_date = "asdfasef"
    if current_user.rang == "Admin":
        user_info_json = json.loads(current_user.user_info)
        if "premium_end_date" in user_info_json:
            print("s")
        else:
            user_info_json["premium_end_date"] = str(datetime.datetime.utcnow())
        current_user.user_info = json.dumps(user_info_json)
        db.session.commit()
        premium_end_date_string = user_info_json["premium_end_date"]
        premium_end_date_object = datetime.datetime.strptime(premium_end_date_string, '%Y-%m-%d %H:%M:%S.%f')
        premium_end_date = premium_end_date_object.strftime('%d. %B %Y')
    return render_template('pages/premium.html', title="Premium", loginRequired=True, premium_end_date=premium_end_date)


@app.route('/mgb/hashtaggeneratorold')
@login_required
def hashtaggeneratorold():
    if current_user.email_confirmed == 'false':
        return redirect(url_for('email_not_confirmed'))
    return render_template('pages/hashtaggenerator.html', title="Hashtag-Generator", loginRequired=True)

@app.route('/mgb/hashtaggenerator')
@login_required
def hashtaggenerator():
    if current_user.rang != "kein Rang":
        user = current_user
        insta_acc1_info = {}

        if user.instaid1:
            try:
                insta_acc1_info = get_user_information_by_username(
                    get_user_by_id(user.instaid1))
                follower = insta_acc1_info['followers']
                print(follower)
            except:
                insta_acc1_info = "Es ist ein Fehler aufgetreten."
        return render_template('pages/hashtaggeneratorpremium.html', title="Hashtag-Generator", loginRequired=True, follower=follower)
    else:
        return render_template('pages/hashtaggeneratornew.html', title="Hashtag-Generator", loginRequired=True)


@app.route('/mgb/accountanalyse', methods=['GET', 'POST'])
@login_required
def accountanalyse():
    if current_user.email_confirmed == 'false':
        return redirect(url_for('email_not_confirmed'))

    if current_user.rang == "kein Rang":
        username = get_user_by_id(current_user.instaid1)
    else:
        username = ""

    analyzer_form = AnalyzerForm()
    if analyzer_form.validate_on_submit():
        username = analyzer_form.instaname.data.replace(
            " ", "")  # Leerzeichen entfernen
        return redirect(url_for('analyzeresults', username=username))
    return render_template('pages/accountanalyse.html', title="Account-Analyse", loginRequired=True, form=analyzer_form, username=username)


@app.route('/mgb/accountanalyse/<username>')
@login_required
def analyzeresults(username):
    if current_user.rang == "kein Rang":
        res = get_user_information_by_username(username)
        user_id = int(res["id"])
    else:
        user_id = "premium"

    if (user_id == "premium") or (user_id == current_user.instaid1):
        print("success")
        if current_user.email_confirmed == 'false':
            return redirect(url_for('email_not_confirmed'))
        user_info_json = json.loads(current_user.user_info)
        try:
            user_info_json["analyzer_usage"] = int(
                user_info_json["analyzer_usage"]) + 1
            print(user_info_json["analyzer_usage"])
        except:
            user_info_json["analyzer_usage"] = 1

        current_user.user_info = json.dumps(user_info_json)
        db.session.commit()
        return render_template('pages/analyzeresults.html', title=str(username), loginRequired=True, username=username)
    else:
        flash("Du kannst nur verbundene Accounts analysieren. Kaufe dir den Premium Rang, um alle Instagram Accounts zu analysieren.", "info")
        return redirect(url_for('accountanalyse'))


@app.route('/timeconverter')
def time_converter():
    return render_template('pages/time_converter.html', title="Time Calculator", nosidebar=True, nav_links_category='no-links')

@app.route('/mgb/eglink')
@login_required
def eglink():
    return render_template('pages/eglink.html', title="EG-Link", loginRequired=True)


@app.route('/eglinknotfound')
def eglinknotfound():
    return render_template('pages/eglinknotfound.html', title="EG-Link")


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
    insta_acc2_info = {}
    insta_acc3_info = {}

    if user.instaid1:
        try:
            insta_acc1_info = get_user_information_by_username(
                get_user_by_id(user.instaid1))
        except:
            insta_acc1_info = "Es ist ein Fehler aufgetreten."

    if user.instaid2:
        try:
            insta_acc2_info = get_user_information_by_username(
                get_user_by_id(user.instaid2))
        except:
            insta_acc2_info['username'] = "Fehler"
    if user.instaid3:
        try:
            insta_acc3_info = get_user_information_by_username(
                get_user_by_id(user.instaid3))
        except:
            insta_acc3_info['username'] = "Fehler"
    user_info_json = json.loads(current_user.user_info)
    if "affiliate_invites" in user_info_json:
        aff_invites = user_info_json["affiliate_invites"]
    else:
        aff_invites = "0"
    return render_template('pages/profile.html', title="Mein Profil", loginRequired=True, insta_acc1_info=insta_acc1_info, insta_acc2_info=insta_acc2_info, insta_acc3_info=insta_acc3_info, aff_invites=aff_invites)


@app.route('/mgb/activate-product/<product_link>', methods=['GET', 'POST'])
@login_required
def activate_product(product_link):
    form = ActivateProductForm()
    if product_link == "zpHv":
        product_name = "EG-Premium (ein Monat)"
    else:
        product_name = "kein name"

    if form.validate_on_submit():
        key = form.product_key.data
        url = "https://payhip.com/api/v1/license/verify?product_link=zpHv&license_key=" + key
        headers = {
            'payhip-api-key': '10e808d815eaecef361713f8a75e4e604b29837e'
        }
        resp = requests.get(url=url, headers=headers).json()
        print(resp)
        try:
            if resp["data"]["enabled"] == True:
                set_premium_end_date(current_user.user_id, 30)
                flash("Herzlichen Glückwunsch, dein Produkt wurde erfolgreich aktiviert!", "success")
                url = "https://payhip.com/api/v1/license/disable"
                headers = {
                    'payhip-api-key': '10e808d815eaecef361713f8a75e4e604b29837e'
                }
                resp = requests.put(url=url, headers=headers, data={"product_link": "zpHv", "license_key": key}).json()
                print(resp)
            else:
                flash("Dieser Product Key ist ungültig. Probiere es bitte mit einem anderen Key oder kontaktiere den Support.", "no-success")
        except:
            pass

    return render_template('pages/activate_product.html', title="Produkt aktivieren", loginRequired=True, form=form, product_name=product_name)


@app.route('/add-insta-acc', methods=['GET', 'POST'])
@login_required
def add_insta_acc():
    form = AddInstaAccForm()

    user_info_json = json.loads(current_user.user_info)
    print(user_info_json)
    if "insta_auth_code" in user_info_json:
        auth_code = user_info_json["insta_auth_code"]
    else:
        user_info_json["insta_auth_code"] = "#" + \
            str(random.randint(1000, 9999))
        auth_code = user_info_json["insta_auth_code"]
        current_user.user_info = json.dumps(user_info_json)
        db.session.commit()

    if current_user.instaid1 and current_user.rang == "kein Rang":
        flash('Du hast bereits einen Instagram Account hinzugefügt. Kaufe den Premium-Rang um bis zu drei Accounts hinzuzufügen.', 'success')
        return redirect('mgb/profile')
    else:
        if form.validate_on_submit():
            user = current_user
            try:
                res = get_user_information_by_username(
                    form.instaname.data.replace(" ", ""))
                bio = res["bio"]
                if auth_code in bio:
                    print("success")

                    if user.instaid1 == None:
                        user.instaid1 = res["id"]
                        db.session.commit()
                    elif user.instaid2 == None:
                        user.instaid2 = res["id"]
                        db.session.commit()
                    elif user.instaid3 == None:
                        user.instaid3 = res["id"]
                        db.session.commit()
                    else:
                        flash(
                            'Du hast bereits die maximale Anzahl an Instagram Accounts hinzugefügt.', 'info')

                    # von der unfollow Liste entfernen, falls vorhanden
                    with open('unfollowliste.json') as f:
                        unfollowliste = json.load(f)
                    if form.instaname.data in unfollowliste:
                        unfollowliste.remove(form.instaname.data)
                    with open('unfollowliste.json', 'w') as f:
                        json.dump(unfollowliste, f)

                    # Account Follow Anfrage stellen
                    with open('anfragenliste.json') as f:
                        anfragenliste = json.load(f)

                    user_info_json = json.loads(current_user.user_info)

                    for eg_acc_name in user_info_json["acc_request_status"]:
                        print("1111111111")
                        if user_info_json["acc_request_status"][eg_acc_name] == "accepted" or user_info_json["acc_request_status"][eg_acc_name] == "pending":
                            print("22222222")
                            anfragenliste[eg_acc_name].append(
                                form.instaname.data)

                    with open('anfragenliste.json', 'w') as f:
                        json.dump(anfragenliste, f)

                    flash('Der Instagram Account wurde hinzugefügt!', 'success')
                else:
                    flash(
                        'Deine Bio enthält nicht den richtigen Code, versuche es bitte erneut.', 'no-success')

            except:
                flash(
                    'Dieser Instagram Account existiert nicht. Versuche es erneut.', 'no-success')
            return redirect(url_for('profile'))
    return render_template('pages/add_insta_acc.html', title='Instagram Account verknüpfen', form=form, insta_auth_code=auth_code)


@app.route('/del-insta-acc/<acc_id>/<insta_username>')
def del_insta_acc(acc_id, insta_username):
    user = current_user
    if acc_id == "1":
        if user.instaid1 and user.instaid2 and user.instaid3:
            user.instaid1 = user.instaid2
            user.instaid2 = user.instaid3
            user.instaid3 = None
        elif user.instaid1 and user.instaid2:
            user.instaid1 = user.instaid2
            user.instaid2 = None
        elif user.instaid1:
            user.instaid1 = None
    if acc_id == "2":
        if user.instaid1 and user.instaid2 and user.instaid3:
            user.instaid2 = user.instaid3
            user.instaid3 = None
        elif user.instaid1 and user.instaid2:
            user.instaid2 = None
    if acc_id == "3":
        if user.instaid1 and user.instaid2 and user.instaid3:
            user.instaid3 = None

    user_info_json = json.loads(current_user.user_info)
    user_info_json["acc_request_status"] = {}
    current_user.user_info = json.dumps(user_info_json)
    db.session.commit()
    flash('Der Instagram Account wurde entfernt.', 'success')
    return redirect(url_for('follow_entfernen_request', insta_username=insta_username))

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


@app.route('/admin/anfragen')
@login_required
def admin_anfragen():
    # Man kommt nur auf die Admin Seite, wenn der Benutzername in der Liste der Admins steht
    if current_user.username in admins:

        with open('anfragenliste.json') as f:
            anfragenliste = json.load(f)

        with open('unfollowliste.json') as f:
            unfollowliste = json.load(f)

        return render_template('pages/admin_anfragen.html', title="Anfragen", loginRequired=True, nosidebar=True, nav_links_category='only-login', anfragenliste=anfragenliste, unfollowliste=unfollowliste)
    else:
        flash('Du hast keine Admin Rechte. Haha.', 'no-success')
        return redirect(url_for('chooseLanguage'))


@app.route('/admin/anfragen/remove/<eg_acc_name>/<insta_username>')
@login_required
def anfrage_entfernen(eg_acc_name, insta_username):
    # Fragenliste bearbeiten
    with open('anfragenliste.json') as f:
        anfragenliste = json.load(f)
    if insta_username in anfragenliste[eg_acc_name]:
        anfragenliste[eg_acc_name].remove(insta_username)
    with open('anfragenliste.json', 'w') as f:
        json.dump(anfragenliste, f)

    # user_info bearbeiten
    user_info_json = json.loads(current_user.user_info)
    user_info_json["acc_request_status"][eg_acc_name] = "accepted"
    current_user.user_info = json.dumps(user_info_json)
    db.session.commit()

    return redirect(url_for('admin_anfragen'))


@app.route('/admin/anfragen/removefollow/<insta_username>')
@login_required
def follow_entfernen(insta_username):

    # Fragenliste bearbeiten
    with open('unfollowliste.json') as f:
        unfollowliste = json.load(f)
    if insta_username in unfollowliste:
        unfollowliste.remove(insta_username)
    with open('unfollowliste.json', 'w') as f:
        json.dump(unfollowliste, f)

    return redirect(url_for('admin_anfragen'))


@app.route('/admin/anfragen/removefollowrequest/<insta_username>')
@login_required
def follow_entfernen_request(insta_username):
    # Fragenliste bearbeiten
    with open('unfollowliste.json') as f:
        unfollowliste = json.load(f)
    if insta_username not in unfollowliste:
        unfollowliste.append(insta_username)
    with open('unfollowliste.json', 'w') as f:
        json.dump(unfollowliste, f)

    # debug
    print(current_user.instaid1)
    print(current_user.instaid2)
    print(current_user.instaid3)
    return redirect(url_for('profile'))


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
            user.email_confirmed = form.email_confirmed.data if form.email_confirmed.data else user.email_confirmed
            user.rang = form.rang.data if form.rang.data else user.rang
            user.eg_level = int(
                form.eg_level.data) if form.eg_level.data else user.eg_level
            user.instaid1 = int(
                form.instaname1.data) if form.instaname1.data else user.instaid1
            user.instaid2 = int(
                form.instaname2.data) if form.instaname2.data else user.instaid2
            user.instaid3 = int(
                form.instaname3.data) if form.instaname3.data else user.instaid3
            db.session.commit()
            flash('Deine Änderungen wurden gespeichert!', 'success')
            return redirect(url_for('admin'))
    else:
        flash('Du hast keine Admin Rechte. Haha.', 'no-success')
        return redirect(url_for('chooseLanguage'))
    flash('Leere Felder bewirken keine Änderung.', 'info')
    return render_template('pages/admin_change_user_details.html', title=f'Account von {user.username} bearbeiten', form=form, user=user)

@app.route('/admin/set-premium', methods=['GET', 'POST'])
@login_required
def admin_set_premium():
    # Man kommt nur auf die Admin Seite, wenn der Benutzername in der Liste der Admins steht
    if current_user.username in admins:
        form = SetPremiumForm()
        if form.validate_on_submit():
            user_id = int(form.user_id.data)
            days = int(form.days.data)
            set_premium_end_date(user_id, days)
        return render_template('pages/admin_set_premium.html', title="Premium", loginRequired=True, nosidebar=True, form=form)
    else:
        flash('Du hast keine Admin Rechte. Haha.', 'no-success')
        return redirect(url_for('chooseLanguage'))