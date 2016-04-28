from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_oauth import OAuth
import json

GOOGLE_CLIENT_ID = "260598740425-jqhva11ahk0nt6ivseim6k68f47k72j5.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "-PRN8gS7RknkPecoV66x_6lE"
# REDIRECT_URI = '/oauth2callback' 

SECRET_KEY = 'development key'
DEBUG = True
 
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
 
    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError
 
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
        data = str(res.read())
        data = json.loads(data)
        pic = data["picture"]
        name = data["name"]
        email = data["email"]
        session["pic"] = pic 
        session["name"] = name
        session["email"] = email
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
 
    return render_template("index.html")
 
 
@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route('/logout')
def logout():
    del session["access_token"]
    # session.pop("pic")
    # session.pop("name")
    # session.pop("email")
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))
 
 
 
@app.route("/oauth2callback")
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))
 
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)