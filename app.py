from flask import Flask, render_template

app = Flask('__name__')

@app.route('/')
def index():
    return render_template('index.html', title = 'Landing Page')

@app.route('/signup')
def signup():
    return render_template('signup.html', title = 'Signup')

@app.route('/login')
def login():
    return render_template('login.html', title = 'Login')

@app.route('/home')
def home():
    return render_template('home.html', title = 'Home', homepage="true")

if __name__ == '__main__':
    app.run(debug=True)