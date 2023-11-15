from flask import render_template, flash, redirect, url_for, request
from app.models import Repository, Issue, User
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Repository, Issue, Status, Category, Severity, Comment
from app.forms import (
    LoginForm, RegistrationForm, 
    RepositoryForm, IssueForm, 
    CommentForm, EditCommentForm, 
    EditRepositoryForm, SettingsFrom,
    EditIssueStatusForm, EditIssueForm)

@app.route('/')
@login_required
def index():
    template = 'core/index.html'
    repository = Repository.query.filter_by(user=current_user)
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
        new_repository = Repository(title=form.title.data, user=current_user, description=form.description.data)
        db.session.add(new_repository)
        db.session.commit()
        flash('Repository created successfully', 'success')
        return redirect(url_for('index'))

    return render_template(template, form=form)

@login_required
@app.route('/repository/<int:repo_id>/details/')
def repository_details(repo_id):
    template = 'core/repository_details.html'
    repo = Repository.query.get(repo_id)
    issues = Issue.query.filter_by(repository_id=repo_id)
    return render_template(template, title="Rep Detail", repo=repo, issues=issues)

@login_required
@app.route('/edit/repository/<int:repository_id>/', methods=['GET', 'POST'])
def edit_repository(repository_id):
    template = 'core/edit_repository.html'
    repository = Repository.query.get(repository_id)

    form = EditRepositoryForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_description = form.description.data
        repository.description = new_description
        db.session.commit()

        flash('Repository update successfully')
        return redirect(url_for('repository_details', repo_id=repository.id))  
    
    form.description.data = repository.description

    return render_template(template, title="Edit Repository", form=form, repository=repository)

@login_required
@app.route('/<string:repository_id>/create_issue/', methods=['GET', 'POST'])
def create_issue(repository_id):
    template = 'core/create_issue.html'
    repository = Repository.query.get(repository_id)
    form = IssueForm()  

    form.severity.choices = [(severity.id, severity.title) for severity in Severity.query.all()]
    form.status.choices = [(status.id, status.title) for status in Status.query.all()]
    form.category.choices = [(category.id, category.title) for category in Category.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        created_by = current_user
        severity_id = form.severity.data
        status_id = form.status.data
        category_id = form.category.data

        severity = Severity.query.get(severity_id)
        status = Status.query.get(status_id)
        category = Category.query.get(category_id)

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
        return redirect(url_for('issues_list', repository_id=repository_id))

    return render_template(template, repository=repository, form=form, title="Issue")

@login_required
@app.route('/<string:repository_id>/issues/')
def issues_list(repository_id):
    template = 'core/issues_list.html'
    issues = Issue.query.filter_by(repository_id=repository_id).order_by(Issue.created_at.desc())
    repository = Repository.query.get(repository_id)
    return render_template(template, title="Issues", issues=issues, repository=repository)

@login_required
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

@login_required
@app.route('/edit/issue/<int:issue_id>/', methods=['GET', 'POST'])
def edit_issue(issue_id):
    template = 'core/edit_issue.html'
    issue = Issue.query.get(issue_id)

    form = EditIssueForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_title = form.title.data
        new_description = form.description.data
        issue.title = new_title
        issue.description = new_description
        db.session.commit()

        flash('Issue updated successfully')
        return redirect(url_for('issues_detail', issue_id=issue.id))

    form.title.data = issue.title
    form.description.data = issue.description

    return render_template(template, title="Edit Repository", form=form)

@app.route('/edit_issue_status/<int:issue_id>/', methods=['POST', 'GET'])
@login_required
def edit_issue_status(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    form = EditIssueStatusForm()

    form.status.choices = [(status.id, status.title) for status in Status.query.all()]
    form.status.default = issue.status.id

    if form.validate_on_submit():
        status_id = form.status.data
        status = Status.query.get(status_id)

        issue.status_id = status_id  
        db.session.commit()

        flash('Issue status updated', 'success')
        return redirect(url_for('issues_detail', issue_id=issue.id))

    return render_template('core/edit_status.html', title='Edit Issue Status', form=form, issue=issue)

@login_required
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

@login_required
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

@app.route('/search', methods=['GET', 'POST'])
def search():
    template = 'core/search_results.html'
    if request.method == 'POST':
        query = request.form.get('query')

        repositories = Repository.query.filter(
            Repository.title.ilike(f"%{query}%")).all()
        issues = Issue.query.filter(Issue.title.ilike(
            f"%{query}%") | Issue.description.ilike(f"%{query}%")).all()
        users = User.query.filter(User.username.ilike(
            f"%{query}%") | User.email.ilike(f"%{query}%")).all()
        
        return render_template(
            template, query=query, 
            repositories=repositories, 
            issues=issues,
            users=users,
            )
    return render_template(template, title='Search')

@app.route('/user/<username>/')
@login_required
def profile(username):
    template = 'core/profile.html'
    user = User.query.filter_by(username=username).first_or_404()
    repos = Repository.query.filter(Repository.user.has(username=username)).all()
    count = len(repos)

    return render_template(template, user=user, repos=repos, title="Profile", count=count)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    template = 'core/settings.html'
    form = SettingsFrom()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.location.data = current_user.location
    return render_template(template, title='Settings',form=form)
