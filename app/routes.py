from flask import render_template, flash, redirect, url_for
from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
def index():
    template = 'core/index.html'
    return render_template(template)

@app.route('/login', methods=['GET', 'POST'])
def login():
    template = 'core/login.html'
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('/'))
    return render_template(template, title='Sign In', form=form)
