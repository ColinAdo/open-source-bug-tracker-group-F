from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

app.app_context().push()

def truncate_words(text, n):
    words = text.split()
    if len(words) > n:
        return ' '.join(words[:n]) + '...'
    return text

app.jinja_env.filters['truncate_words'] = truncate_words

from app import routes, models