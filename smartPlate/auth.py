# auth.py
from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager
from models import User

# Create the auth Blueprint
auth = Blueprint('auth', __name__)

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose another.')
            return redirect(url_for('auth.register'))
        # Use the default hashing method (pbkdf2:sha256)
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')

# Logout route
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))