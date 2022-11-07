'''
AEIOU : Brian Chen, Weichen Liu, Vansh Saboo
11/02/22
'''

from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)


app.secret_key = os.urandom(12)

users = {'m':'donky'}


@app.route("/")
def index():
    return render_template('homepage.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = request.args.get('username')
        password = request.args.get('password')
        print(f"User entered: {user}")
        print(f"Password entered: {password}")
        if user not in users.keys(): #check if user exists
            error = "User DNE"
            return render_template('login.html',
            error=error)
        if password != users[user]: #check if password matches user
            error = "Wrong Password"
            return render_template('login.html',
            error=error)
        session["username"] = user
        session['logged_in'] = True
        return redirect(url_for('index'))  #redirects to home page


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()