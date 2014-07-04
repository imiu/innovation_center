from . import root
from flask import render_template

@root.route('/')
def home():
    return render_template('base.html')