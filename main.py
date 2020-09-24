from flask import Flask, render_template

app = Flask(__name__)

# Startseite (Landing Page)
@app.route('/')
def landingPage():
    return render_template('pages/landingpage.html', isLandingPage = True)

# Alle Seiten im Mitgliederbereich
@app.route('/mgb')
def mgb():
    return render_template('pages/mgb.html', isLandingPage = False)
@app.route('/mgb/profile')
def profile():
    return render_template('pages/profile.html', isLandingPage = False)

if __name__ == '__main__':
    app.run(port=1000, debug=True)