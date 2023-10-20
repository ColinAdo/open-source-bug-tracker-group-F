from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from flask import render_template
from app.models import User, Repository
from app import app
from app.forms import LoginForm, RegistrationForm, RepositoryForm
from app import db

@app.route('/')
@login_required
def index():
    template = 'core/index.html'
    repository = Repository.query.all()
    return render_template(template, title='Home Page', repository=repository)

@app.route('/register', methods=['GET', 'POST'])
def register():
    template = 'auths/register.html'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template(template, title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    template = 'auths/login.html'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template(template, title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create/repository/', methods=['GET', 'POST'])
@login_required
def create_repository():
    template = 'core/create_repository.html'
    form = RepositoryForm()
    if form.validate_on_submit():
        new_repository = Repository(title=form.title.data, description=form.description.data)
        db.session.add(new_repository)
        db.session.commit()
        flash('Repository created successfully', 'success')
        return redirect(url_for('index'))

    return render_template(template, form=form)

@app.route('/repository/<int:repo_id>/details/')
def repository_details(repo_id):
    template = 'core/repository_details.html'
    repo = Repository.query.get(repo_id)
    return render_template(template, title="Rep Detail", repo=repo)
