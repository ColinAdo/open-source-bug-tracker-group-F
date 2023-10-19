from flask import render_template
from app import app

@app.route('/')
@app.route('/home')
def index():
    template = 'core/index.html'
    return render_template(template)
