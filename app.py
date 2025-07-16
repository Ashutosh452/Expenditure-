from flask import Flask, render_template, request, redirect, session
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERNAME = 'admin'
PASSWORD = 'password123'

FILENAME = 'expenditure.csv'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')
    try:
        with open(FILENAME, newline='') as f:
            data = list(csv.reader(f))
    except FileNotFoundError:
        data = []
    return render_template('index.html', records=data)

@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        return redirect('/')
    head = request.form['head']
    subhead = request.form['subhead']
    amount = request.form['amount']
    with open(FILENAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([head, subhead, amount])
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')
