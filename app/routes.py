from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, admins, eg_boost_runden
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required


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


'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('mgb'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account für {form.username.data} erfolgreich erstellt!', 'success')
        return redirect(url_for('mgb'))
    return render_template('pages/register.html', title="Registrieren", form=form, nosidebar=True, nav_links_category='no-links')
'''


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
    return render_template('pages/egboost.html', title="EG-Boost", loginRequired=True, eg_boost_runden=eg_boost_runden)


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

# Nur für Admins
@app.route('/admin')
@login_required
def admin():
    # Man kommt nur auf die Admin Seite, wenn der Benutzername in der Liste der Admins steht
    if current_user.username in admins:
        users = User.query.all()
        #register_date=user.date_created.strftime('%d')
        return render_template('pages/admin.html', title="Admin-Dashboard", loginRequired=True, nosidebar=True, nav_links_category='only-login', users=users)
    else:
        flash('Du hast keine Admin Rechte. Haha.', 'no-success')
        return redirect(url_for('landingPage'))


@app.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    # Man kommt nur auf die Admin Seite, wenn der Benutzername in der Liste der Admins steht
    if current_user.username in admins:
        if current_user.id != 1:
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
