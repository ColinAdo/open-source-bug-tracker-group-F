from enum import Enum as OptionEnum
from datetime import datetime
from sqlalchemy import Enum
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

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
    
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True )
    description = db.Column(db.String(500), index=True)
    severity = db.Column(db.Integer, db.ForeignKey('severity.id'), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

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
    

