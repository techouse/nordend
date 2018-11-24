from kilc import app


@app.route('/')
@app.route('/index')
def index():
    return 'Oh Hai!'
