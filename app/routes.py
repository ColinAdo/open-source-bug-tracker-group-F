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

# This is route for home page
@app.route('/')
@login_required
def index():
    template = 'core/index.html'
    # getting sll the repository based on the logged in user
    repository = Repository.query.filter_by(user=current_user)
    return render_template(template, title='Home Page', repository=repository)

# This is route for user registration 
@app.route('/register', methods=['GET', 'POST'])
def register():
    template = 'auths/register.html'
    # checking if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # creating user 
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # display success message after successful registration
        flash('Congratulations, you are now a registered user!')
        # redirect them to login page
        return redirect(url_for('login'))
    return render_template(template, title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    template = 'auths/login.html'
    # check if the user is already logged in
    if current_user.is_authenticated:
        # then redirect to home page
        return redirect(url_for('index'))
    # display the login form to the template so that the user can login
    form = LoginForm()
    # check id the form is valid on submission
    if form.validate_on_submit():
        # get the current user based on the data passed in the form
        user = User.query.filter_by(username=form.username.data).first()
        # check if the user does not already exist or if the password is not correct
        if user is None or not user.check_password(form.password.data):
            # display the error message to the user 
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template(template, title='Sign In', form=form)

# this route is to logout the user from the site
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# This route is to create repositories
@app.route('/create/repository/', methods=['GET', 'POST'])
@login_required
def create_repository():
    template = 'core/create_repository.html'
    # display the form for the user to create a repository
    form = RepositoryForm()
    # checking the data the user provided is correct
    if form.validate_on_submit():
        # create the repository
        new_repository = Repository(title=form.title.data, user=current_user, description=form.description.data)
        # add the new repository to the database
        db.session.add(new_repository)
        db.session.commit()
        # display message and redirect them to the home page
        flash('Repository created successfully', 'success')
        return redirect(url_for('index'))

    return render_template(template, form=form)

# This route is to display the details of an individual repository
@login_required
@app.route('/repository/<int:repo_id>/details/')
def repository_details(repo_id):
    template = 'core/repository_details.html'
    # getting the individual repo
    repo = Repository.query.get(repo_id)
    # getting all the issue associated with the repository
    issues = Issue.query.filter_by(repository_id=repo_id)
    # pass them to template
    return render_template(template, title="Rep Detail", repo=repo, issues=issues)

# This route is to edit the description of a repository
@login_required
@app.route('/edit/repository/<int:repository_id>/', methods=['GET', 'POST'])
def edit_repository(repository_id):
    template = 'core/edit_repository.html'
    # Getting the individual repository
    repository = Repository.query.get(repository_id)

    # Display the repository form
    form = EditRepositoryForm()

    # Checking if the form is submitted under POST or if its valid to create the new repository
    if request.method == 'POST' and form.validate_on_submit():
        new_description = form.description.data
        repository.description = new_description
        db.session.commit()

        # Display the message
        flash('Repository update successfully')
        return redirect(url_for('repository_details', repo_id=repository.id))  
    
    form.description.data = repository.description

    return render_template(template, title="Edit Repository", form=form, repository=repository)

# This route is used to create a new issue based on a given repository
@login_required
@app.route('/<string:repository_id>/create_issue/', methods=['GET', 'POST'])
def create_issue(repository_id):
    template = 'core/create_issue.html'

    # Getting a repository 
    repository = Repository.query.get(repository_id)

    form = IssueForm()  

    """ displaying the the list of severity, status and category as select list in the form
    for user to select """
    form.severity.choices = [(severity.id, severity.title) for severity in Severity.query.all()]
    form.status.choices = [(status.id, status.title) for status in Status.query.all()]
    form.category.choices = [(category.id, category.title) for category in Category.query.all()]

    # Checking if anything is submitted correctly
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

        # creating new issue
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

# This route is to display all issues associated with a repository
@login_required
@app.route('/<string:repository_id>/issues/')
def issues_list(repository_id):
    template = 'core/issues_list.html'
    # Getting all issues associated with a repository
    issues = Issue.query.filter_by(repository_id=repository_id).order_by(Issue.created_at.desc())
    # Getting the individual repositories 
    repository = Repository.query.get(repository_id)
    return render_template(template, title="Issues", issues=issues, repository=repository)

# This route is to display the distails of an individual issue of a given repository
@login_required
@app.route('/issues/<int:issue_id>/', methods=['GET', 'POST'])
def issues_detail(issue_id):
    template = 'core/issues_detail.html'
    # Getting the issue based on unique identifier passed on url i.e issue_id
    issue = Issue.query.get(issue_id)
    # Getting all comment associatted with the issue
    comments = Comment.query.filter_by(issue_id=issue_id)

    # Display the comment form
    form = CommentForm()
    if request.method == 'POST' and form.validate_on_submit():
        text = form.text.data

        # Creating new comment after validations
        comment = Comment(issue_id=issue_id, user_id=current_user.id, text=text)
        db.session.add(comment)
        db.session.commit()

        flash('You Commented')
        return redirect(url_for('issues_detail', issue_id=issue_id))

    return render_template(template, title="Issues Detail", issue=issue, form=form, comments=comments)  

# This route is to edit the issue
@login_required
@app.route('/edit/issue/<int:issue_id>/', methods=['GET', 'POST'])
def edit_issue(issue_id):
    template = 'core/edit_issue.html'
    # Getting individual issue
    issue = Issue.query.get(issue_id)

    # Display the form to edit the issue
    form = EditIssueForm()

    # Checking if anything is well with the form
    if request.method == 'POST' and form.validate_on_submit():
        new_title = form.title.data
        new_description = form.description.data
        issue.title = new_title
        issue.description = new_description
        db.session.commit()

        flash('Issue updated successfully')
        return redirect(url_for('issues_detail', issue_id=issue.id))

    # Creating new instance of Issue
    form.title.data = issue.title
    form.description.data = issue.description

    return render_template(template, title="Edit Repository", form=form)

# This route is used to edit a status of a give issue
@app.route('/edit_issue_status/<int:issue_id>/', methods=['POST', 'GET'])
@login_required
def edit_issue_status(issue_id):
    # Getting the individual issue
    issue = Issue.query.get_or_404(issue_id)
    form = EditIssueStatusForm()

    # Display the choices in the form with their values
    form.status.choices = [(status.id, status.title) for status in Status.query.all()]
    form.status.default = issue.status.id

    # Validating the form 
    if form.validate_on_submit():
        status_id = form.status.data
        status = Status.query.get(status_id)

        issue.status_id = status_id  
        db.session.commit()

        flash('Issue status updated', 'success')
        return redirect(url_for('issues_detail', issue_id=issue.id))

    return render_template('core/edit_status.html', title='Edit Issue Status', form=form, issue=issue)

# This route is to edit comment posted by a user
@login_required
@app.route('/edit/comment/<int:comment_id>/', methods=['GET', 'POST'])
def edit_comment(comment_id):
    template = 'core/edit_comment.html'
    # Getting the comment
    comment = Comment.query.get(comment_id)

    # Display the form for editing the comment
    form = EditCommentForm()


    if request.method == 'POST' and form.validate_on_submit():
        new_text = form.text.data
        comment.text = new_text
        db.session.commit()

        flash('Comment updated successfully')
        return redirect(url_for('issues_detail', issue_id=comment.issue_id))  

    # Display the comment data itself in the form    
    form.text.data = comment.text

    return render_template(template, title="Edit Comment", form=form)

# This route is used to delete a comment
@login_required
@app.route('/delete/comment/<int:comment_id>/', methods=['GET', 'POST'])
def delete_comment(comment_id):
    # Getting the comment that need to be deleted 
    comment = Comment.query.get(comment_id)

    # Check if the comment is present in the database
    if comment:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully')
    else:
        flash('Comment not found')

    return redirect(url_for('issues_detail', issue_id=comment.issue_id))

# This route is used to search in the issue tracker
@app.route('/search', methods=['GET', 'POST'])
def search():
    template = 'core/search_results.html'
    # Checking if the mothod is passed under POST
    if request.method == 'POST':
        # We grasp the text inputted by the user
        query = request.form.get('query')

        # Check if the text inputted by the user is somehow like that of repository
        repositories = Repository.query.filter(
            Repository.title.ilike(f"%{query}%")).all()
        
        # Check if the text inputted by the user is somehow like that of issue
        issues = Issue.query.filter(Issue.title.ilike(
            f"%{query}%") | Issue.description.ilike(f"%{query}%")).all()
        
        # Check if the text inputted by the user is somehow like that of user
        users = User.query.filter(User.username.ilike(
            f"%{query}%") | User.email.ilike(f"%{query}%")).all()

        # Pass them int a tempate to be displayed
        return render_template(
            template, query=query, 
            repositories=repositories, 
            issues=issues,
            users=users,
            )
    return render_template(template, title='Search')

# This route is used to display user profile information
@app.route('/user/<username>/')
@login_required
def profile(username):
    template = 'core/profile.html'
    # Getting the user accessing the page
    user = User.query.filter_by(username=username).first_or_404()
    # Getting the repository created by the user
    repos = Repository.query.filter(Repository.user.has(username=username)).all()
    count = len(repos)

    return render_template(template, user=user, repos=repos, title="Profile", count=count)

# This route is used to edit the profile information such bio, location
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    template = 'core/settings.html'
    # Display the form for editing profile information
    form = SettingsFrom()
    # Checking if form is valid
    if form.validate_on_submit():
        # Updating the profile information to the database
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.commit()
        # Tell the user the update is successful
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    
    # If the form is not valid, then display the user information
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.location.data = current_user.location
    # Pass the template
    return render_template(template, title='Settings',form=form)
