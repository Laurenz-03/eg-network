from flask import Flask, render_template

app = Flask(__name__)

# Startseite (Landing Page)
@app.route('/')
def landingPage():
    return render_template('pages/landingpage.html', isLandingPage = True)

@app.route('/login')
def login():
    return render_template('pages/login.html')
@app.route('/impressum')
def impressum():
    return render_template('pages/impressum.html')

# Alle Seiten im Mitgliederbereich
@app.route('/mgb')
def mgb():
    return render_template('pages/mgb.html', loginRequired=True)

@app.route('/egboost')
def egboost():
    return render_template('pages/egboost.html', loginRequired=True)

@app.route('/mgb/tools')
def tools():
    return render_template('pages/tools.html', loginRequired=True)
    
@app.route('/mgb/profile')
def profile():
    return render_template('pages/profile.html', loginRequired=True)

if __name__ == '__main__':
    app.run(port=1000, debug=True)