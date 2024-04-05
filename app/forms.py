from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, 
    BooleanField, SubmitField, 
    TextAreaField,SelectField )

# Login form route
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign-In')

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign-Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Repository Form
class RepositoryForm(FlaskForm):
    title = StringField('Repository Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Repository')

#  Edit repository form
class EditRepositoryForm(FlaskForm):
    description = TextAreaField('Description')
    submit = SubmitField('Edit Repository')

#  Issue repository form
class IssueForm(FlaskForm):
    title = StringField('Issue title', validators=[DataRequired()])
    description = TextAreaField('Description')
    severity = SelectField('Severity', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', coerce=int, validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Issue')

#  Comment repository form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

#  Edit Comment form
class EditCommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Edit Comment')

#  Edit settings form
class SettingsFrom(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = StringField('About me', validators=[Length(min=0, max=140)])
    location = StringField('Location', validators=[Length(min=0, max=20)])
    submit = SubmitField('Submit')

#  Edit issue status form
class EditIssueStatusForm(FlaskForm):
    status = SelectField('Status', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

#  Edit issue form
class EditIssueForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')