from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_user, current_user, login_required
from .forms import LoginForm, RegistrationForm
from .models import User
from ..extensions import db

from . import user

@user.route('/login', methods=['GET', 'POST'])
def login():
    """ log the user in """
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data.lower()).first()
        if u is not None and u.verify_password(form.password.data):
            login_user(u)
            flash('successfully logged in', 'success')
            return redirect(url_for('root.home'))
        flash('invalid login')
    return render_template('user/login.html', form=form)


@user.route('/logout')
def logout():
    """ log the user out """
    logout_user()
    flash('you were successfully logged out')
    return redirect(url_for('root.home'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    """ register a new user using the form """
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data.lower(),
            first_name=form.first_name.data.lower(),
            last_name=form.last_name.data.lower(),
            username=form.username.data.lower(),
            password=form.password.data
        )
        db.session.add(new_user)
        flash('successfully registered!', 'success')
        print(User.query.all())
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)