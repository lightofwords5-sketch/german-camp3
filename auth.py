# auth.py

from flask import Flask, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # Either 'admin' or 'student'

    def __repr__(self):
        return f'<User {self.username}>'

# Role-based access control decorator
def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session or session['role'] != role:
                flash('You do not have permission to access this page.')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@role_required('admin')  # Admin only view
def dashboard():
    return 'Welcome to the admin dashboard!'

if __name__ == '__main__':
    app.run(debug=True)