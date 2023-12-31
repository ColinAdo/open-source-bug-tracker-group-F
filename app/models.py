from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import login
from app import db
from hashlib import md5

# User model 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(250))

    about_me = db.Column(db.String(140))
    location = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

# Issue severity model
class Severity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True) 

    def __repr__(self):
        return '<Severity {}>'.format(self.title)
    
# Issue status model
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True) 

    def __repr__(self):
        return '<Status {}>'.format(self.title)
    
# Issue category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)

    def __repr__(self):
        return '<Category {}>'.format(self.title)
    
# Repository model
class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='issue_repository_fk'))
    user = db.relationship('User', backref='repositories')
    issues = db.relationship('Issue', backref='repository', lazy='dynamic', foreign_keys='Issue.repository_id')
    
    def __repr__(self):
        return '<Repository {}>'.format(self.title)

# Issue model
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    description = db.Column(db.String(500), index=True)

    status_id = db.Column(db.Integer, db.ForeignKey(
        'status.id', name='issue_status_fk'), nullable=False)
    status = db.relationship('Status', backref='issues')

    severity_id = db.Column(db.Integer, db.ForeignKey(
        'severity.id', name='issue_severity_fk'), nullable=False)
    severity = db.relationship('Severity', backref='issues')

    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id', name='issue_category_fk'), nullable=False)
    category = db.relationship('Category', backref='issues') 

    created_by_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', name='issue_user_fk'), nullable=False)
    created_by = db.relationship(
        'User', backref='created_issues', foreign_keys=[created_by_id])

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    repository_id = db.Column(db.Integer, db.ForeignKey(
        'repository.id', name='issue_repository_fk'), nullable=False)

    def __repr__(self):
        return '<Issue {}>'.format(self.title)
    
# Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='comment_user_fk'), nullable=False)
    user = db.relationship('User', backref='comment_user', foreign_keys=[user_id])
    text = db.Column(db.String(500), index=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.text)
    
# get user id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
