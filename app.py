from flask import Flask, render_template

app = Flask(__name__)

# Startseite (Landing Page)
@app.route('/')
def landingPage():
    return render_template('pages/landingpage.html', title="Startseite", isLandingPage=True)


@app.route('/login')
def login():
    return render_template('pages/login.html', title="Einloggen")


@app.route('/impressum')
def impressum():
    return render_template('pages/impressum.html', title="Impressum")

# Alle Seiten im Mitgliederbereich
@app.route('/mgb')
def mgb():
    return render_template('pages/mgb.html', title="Home", loginRequired=True)


@app.route('/egboost')
def egboost():
    return render_template('pages/egboost.html', title="EG-Boost", loginRequired=True)


@app.route('/mgb/tools')
def tools():
    return render_template('pages/tools.html', title="Tools", loginRequired=True)

@app.route('/mgb/premium')
def premium():
    return render_template('pages/premium.html', title="Premium", loginRequired=True)

@app.route('/mgb/hashtaggenerator')
def hashtaggenerator():
    return render_template('pages/hashtaggenerator.html', title="Hashtag-Generator", loginRequired=True)

@app.route('/mgb/accountanalyse')
def accountanalyse():
    return render_template('pages/accountanalyse.html', title="Account-Analyse", loginRequired=True)

@app.route('/mgb/shoutoutmatcher')
def shoutoutmatcher():
    return render_template('pages/shoutoutmatcher.html', title="Shoutout-Matcher", loginRequired=True)

@app.route('/mgb/ebookskurse')
def ebookskurse():
    return render_template('pages/ebookskurse.html', title="eBooks & Kurse", loginRequired=True)

@app.route('/mgb/profile')
def profile():
    return render_template('pages/profile.html', title="Mein Profil", loginRequired=True)

app.config.update(TEMPLATES_AUTO_RELOAD = True)
if __name__ == '__main__':
    app.run(port=1000, debug=True)
