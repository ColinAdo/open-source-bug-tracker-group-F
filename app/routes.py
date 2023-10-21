from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required, current_user
from flask import render_template
from app.models import User, Repository, Issue, Status, Category, Severity, Comment
from app import app
from app.forms import LoginForm, RegistrationForm, RepositoryForm, IssueForm, CommentForm, EditCommentForm, EditRepositoryForm
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
    issues = Issue.query.filter_by(repository_id=repo_id)
    return render_template(template, title="Rep Detail", repo=repo, issues=issues)

@app.route('/edit/repository/<int:repository_id>/', methods=['GET', 'POST'])
def edit_repository(repository_id):
    template = 'core/edit_repository.html'
    repository = Repository.query.get(repository_id)

    form = EditRepositoryForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_description = form.description.data
        repository.description = new_description
        db.session.commit()

        flash('Comment updated successfully')
        return redirect(url_for('repository_details', repo_id=repository.id))  
    
    form.description.data = repository.description

    return render_template(template, title="Edit Repository", form=form)

@app.route('/<string:repository_id>/create_issue/', methods=['GET', 'POST'])
def create_issue(repository_id):
    template = 'core/create_issue.html'
    repository = Repository.query.get(repository_id)
    form = IssueForm()  

    # Populate form choices for Severity, Status, and Category
    form.severity.choices = [(severity.id, severity.title) for severity in Severity.query.all()]
    form.status.choices = [(status.id, status.title) for status in Status.query.all()]
    form.category.choices = [(category.id, category.title) for category in Category.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        created_by = current_user.id
        severity = form.severity.data
        status = form.status.data
        category = form.category.data

        issue = Issue(
            title=title,
            description=description,
            severity=severity,
            status=status,
            created_by=created_by,
            category=category,
            repository_id=repository_id
        )

        db.session.add(issue)
        db.session.commit()

        flash('Issue created successfully')
        return redirect(url_for('create_issue', repository_id=repository_id))

    return render_template(template, repository=repository, form=form, title="Issue")

@app.route('/<string:repository_id>/issues/')
def issues_list(repository_id):
    template = 'core/issues_list.html'
    issues = Issue.query.filter_by(repository_id=repository_id)
    return render_template(template, title="Issues", issues=issues)

@app.route('/issues/<int:issue_id>/', methods=['GET', 'POST'])
def issues_detail(issue_id):
    template = 'core/issues_detail.html'
    issue = Issue.query.get(issue_id)
    comments = Comment.query.filter_by(issue_id=issue_id)

    form = CommentForm()
    if request.method == 'POST' and form.validate_on_submit():
        text = form.text.data

        comment = Comment(issue_id=issue_id, user_id=current_user.id, text=text)
        db.session.add(comment)
        db.session.commit()

        flash('You Commented')
        return redirect(url_for('issues_detail', issue_id=issue_id))

    return render_template(template, title="Issues Detail", issue=issue, form=form, comments=comments)  

@app.route('/edit/comment/<int:comment_id>/', methods=['GET', 'POST'])
def edit_comment(comment_id):
    template = 'core/edit_comment.html'
    comment = Comment.query.get(comment_id)

    form = EditCommentForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_text = form.text.data
        comment.text = new_text
        db.session.commit()

        flash('Comment updated successfully')
        return redirect(url_for('issues_detail', issue_id=comment.issue_id))  
    
    form.text.data = comment.text

    return render_template(template, title="Edit Comment", form=form)

@app.route('/delete/comment/<int:comment_id>/', methods=['GET', 'POST'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully')
    else:
        flash('Comment not found')

    return redirect(url_for('issues_detail', issue_id=comment.issue_id))  