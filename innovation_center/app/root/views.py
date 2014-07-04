from . import root
from flask import render_template

@root.route('/')
def homepage():
    return render_template('homepage.html')