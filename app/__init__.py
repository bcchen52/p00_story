'''
AEIOU : Brian Chen, Weichen Liu, Vansh Saboo
11/02/22
'''

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")