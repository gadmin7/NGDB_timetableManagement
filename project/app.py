from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['timetable_database']

# Sample user data (for demonstration purposes)
users = [
    {'username': 'admin', 'password': 'admin', 'role': 'admin'},
    {'username': 'teacher1', 'password': 'teacher1', 'role': 'teacher'},
    {'username': 'student1', 'password': 'student1', 'role': 'student'}
]

# Routes
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((u for u in users if u['username'] == username and u['password'] == password), None)

        if user:
            return redirect(url_for(user['role']))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html', error=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        # Validate password match
        if password != confirm_password:
            return render_template('login.html', error='Passwords do not match')

        # Check if the username is already taken
        if any(u['username'] == username for u in users):
            return render_template('login.html', error='Username is already taken')

        # Add the new user to the users list (in-memory for demonstration purposes)
        new_user = {'username': username, 'password': password, 'role': role}
        users.append(new_user)

        # Redirect to login page after successful signup
        return redirect(url_for('login'))

    return render_template('signup.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
