from flask import render_template, Flask

app = Flask(__name__)


@app.route('/Login')
def login():
    return render_template('login.html')

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)