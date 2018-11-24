from flask import render_template
from kilc import app


@app.route('/')
@app.route('/index')
def index():
    context = {'user': {'name': 'Klemen'}}

    return render_template('index.html', **context)
