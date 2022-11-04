'''
AEIOU : Brian Chen, Weichen Liu, Vansh Saboo
11/02/22
'''

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('homepage.html')


@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()