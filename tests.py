from flask import Flask
from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Severity, Status, Category, Repository, Issue, Comment
from app.forms import LoginForm
from config import Config, TestConfig
from flask_login import login_user

# Tast case for testing User model
class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig) 
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

# Tast case for testing Severity model
class SeverityModelCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestConfig)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_severity(self):
        title = "High"
        severity = Severity(title=title)
        db.session.add(severity)
        db.session.commit()

        queried_severity = Severity.query.filter_by(title=title).first()
        self.assertIsNotNone(queried_severity)
        self.assertEqual(queried_severity.title, title)

    def test_repr_method(self):
        title = "Medium"
        severity = Severity(title=title)
        db.session.add(severity)
        db.session.commit()

        queried_severity = Severity.query.filter_by(title=title).first()
        expected_repr = f'<Severity {queried_severity.title}>'
        self.assertEqual(str(queried_severity), expected_repr)

# Tast case for testing Status model
class StatusModelCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestConfig)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_status(self):
        title = "Open"
        status = Status(title=title)
        db.session.add(status)
        db.session.commit()

        queried_status = Status.query.filter_by(title=title).first()
        self.assertIsNotNone(queried_status)
        self.assertEqual(queried_status.title, title)

    def test_repr_method(self):
        title = "Closed"
        status = Status(title=title)
        db.session.add(status)
        db.session.commit()

        queried_status = Status.query.filter_by(title=title).first()
        expected_repr = f'<Status {queried_status.title}>'
        self.assertEqual(str(queried_status), expected_repr)

# Tast case for testing Category model
class CategoryModelCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestConfig)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_category(self):
        title = "Bug"
        category = Category(title=title)
        db.session.add(category)
        db.session.commit()

        queried_category = Category.query.filter_by(title=title).first()
        self.assertIsNotNone(queried_category)
        self.assertEqual(queried_category.title, title)

    def test_repr_method(self):
        title = "Feature"
        category = Status(title=title)
        db.session.add(category)
        db.session.commit()

        queried_category = Status.query.filter_by(title=title).first()
        expected_repr = f'<Status {queried_category.title}>'
        self.assertEqual(str(queried_category), expected_repr)

# Tast case for testing Repository model
class RepositoryModelCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestConfig)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_repository(self):
        user = User(username='testuser', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        repository = Repository(title='Test Repository',
                                description='Test Description', user_id=user.id)
        db.session.add(repository)
        db.session.commit()

        queried_repository = Repository.query.filter_by(
            title='Test Repository').first()
        self.assertIsNotNone(queried_repository)
        self.assertEqual(queried_repository.description, 'Test Description')
        self.assertEqual(queried_repository.user.username, 'testuser')

    def test_created_at_default_value(self):
        repository = Repository(title='Test Repository')
        db.session.add(repository)
        db.session.commit()

        queried_repository = Repository.query.filter_by(
            title='Test Repository').first()
        self.assertIsNotNone(queried_repository)
        self.assertIsInstance(queried_repository.created_at, datetime)

    def test_repr_method(self):
        repository = Repository(title='Test Repository')
        db.session.add(repository)
        db.session.commit()

        queried_repository = Repository.query.filter_by(
            title='Test Repository').first()
        expected_repr = f'<Repository {queried_repository.title}>'
        self.assertEqual(str(queried_repository), expected_repr)

# Tast case for testing Issue model
class IssueModelCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestConfig)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_issue(self):
        status = Status(title='Open')
        severity = Severity(title='High')
        category = Category(title='Bug')
        user = User(username='testuser', email='testuser@example.com')
        repository = Repository(title='Test Repository', user=user)

        db.session.add_all([status, severity, category, user, repository])
        db.session.commit()

        issue = Issue(title='Test Issue', description='Test Description', status_id=status.id,
                      severity_id=severity.id, category_id=category.id, created_by_id=user.id, repository_id=repository.id)

        db.session.add(issue)
        db.session.commit()

        queried_issue = Issue.query.filter_by(title='Test Issue').first()
        self.assertIsNotNone(queried_issue)
        self.assertEqual(queried_issue.description, 'Test Description')
        self.assertEqual(queried_issue.status.title, 'Open')
        self.assertEqual(queried_issue.severity.title, 'High')
        self.assertEqual(queried_issue.category.title, 'Bug')
        self.assertEqual(queried_issue.created_by.username, 'testuser')
        self.assertEqual(queried_issue.repository.title, 'Test Repository')

    def test_created_at_default_value(self):
        status = Status(title='Open')
        severity = Severity(title='High')
        category = Category(title='Bug')
        user = User(username='testuser', email='testuser@example.com')
        repository = Repository(title='Test Repository', user=user)

        db.session.add_all([status, severity, category, user, repository])
        db.session.commit()

        issue = Issue(title='Test Issue', description='Test Description', 
                    status_id=status.id, severity_id=severity.id,
                    category_id=category.id, created_by_id=user.id,
                    created_at=datetime.utcnow(), repository_id=repository.id)

        db.session.add(issue)
        db.session.commit()

        queried_issue = Issue.query.filter_by(title='Test Issue').first()
        self.assertIsNotNone(queried_issue)
        self.assertIsInstance(queried_issue.created_at, datetime)


    def test_repr_method(self):
        status = Status(title='Open')
        severity = Severity(title='High')
        category = Category(title='Bug')
        user = User(username='testuser', email='testuser@example.com')
        repository = Repository(title='Test Repository', user=user)

        db.session.add_all([status, severity, category, user, repository])
        db.session.commit()

        issue = Issue(title='Test Issue', description='Test Description', 
                    status_id=status.id, severity_id=severity.id,
                    category_id=category.id, created_by_id=user.id,
                    created_at=datetime.utcnow(), repository_id=repository.id)

        db.session.add(issue)
        db.session.commit()

        queried_issue = Issue.query.filter_by(title='Test Issue').first()
        self.assertIsNotNone(queried_issue)
        self.assertIsInstance(queried_issue.created_at, datetime)

# Tast case for testing Comment model

# Test case for testing DATABASE URI
class TestConfig(unittest.TestCase):

    def test_secret_key(self):
        # Check if SECRET_KEY is set or using the default value
        config = Config()
        self.assertIsNotNone(config.SECRET_KEY)
        self.assertIsInstance(config.SECRET_KEY, str)

    def test_database_uri(self):
        # Check if SQLALCHEMY_DATABASE_URI is set or using the default value
        config = Config()
        self.assertIsNotNone(config.SQLALCHEMY_DATABASE_URI)
        self.assertIsInstance(config.SQLALCHEMY_DATABASE_URI, str)

    def test_track_modifications(self):
        # Check if SQLALCHEMY_TRACK_MODIFICATIONS is set and is False
        config = Config()
        self.assertIsNotNone(config.SQLALCHEMY_TRACK_MODIFICATIONS)
        self.assertFalse(config.SQLALCHEMY_TRACK_MODIFICATIONS)

# Set up a Flask app for testing
app = Flask(__name__)

# Disable CSRF protection for testing
app.config['WTF_CSRF_ENABLED'] = False 

# Tast case for testing LoginForm
class TestLoginForm(unittest.TestCase):

    def test_required_fields(self):
        with app.test_request_context():
            form = LoginForm()
            self.assertFalse(form.validate())
            self.assertIn('This field is required.', form.username.errors)
            self.assertIn('This field is required.', form.password.errors)

    def test_valid_data(self):
        with app.test_request_context():
            form = LoginForm(username='testuser', password='testpassword')
            self.assertTrue(form.validate())

    def test_optional_field(self):
        with app.test_request_context():
            form = LoginForm(username='testuser',
                             password='testpassword', remember_me=True)
            self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main(verbosity=2)
