from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum as OptionEnum
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Enum
from app import login
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Severity(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    class TitleOptions(OptionEnum):
        CRITICAL = "critical"
        MAJOR = "major"
        MINOR = "minor"

    title = db.Column(Enum(TitleOptions), index=True) 

    def __repr__(self):
        return '<Severity {}>'.format(self.title)
    

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    class TitleOptions(OptionEnum):
        CRITICAL = "open"
        MAJOR = "in progress"
        MINOR = "closed"

    title = db.Column(Enum(TitleOptions), index=True)

    def __repr__(self):
        return '<Status {}>'.format(self.title)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    class TitleOptions(OptionEnum):
        CRITICAL = "bug"
        MAJOR = "feature"
        MINOR = "enhancement"

    title = db.Column(Enum(TitleOptions), index=True)

    def __repr__(self):
        return '<Category {}>'.format(self.title)
    
class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    issues = db.relationship('Issue', backref='repository', lazy='dynamic', foreign_keys='Issue.repository_id')
    
    def __repr__(self):
        return '<Repository {}>'.format(self.title)

    
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    description = db.Column(db.String(500), index=True)
    severity = db.Column(db.Integer, db.ForeignKey('severity.id', name='issue_severity_fk'), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('status.id', name='issue_status_fk'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', name='issue_user_fk'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id', name='issue_category_fk'), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id', name='issue_repository_fk'), nullable=False)

    def __repr__(self):
        return '<Issue {}>'.format(self.title)

    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(500), index=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.text)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
