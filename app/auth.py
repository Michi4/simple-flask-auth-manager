from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
import re

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            flash('Invalid username format.', 'danger')
            return render_template('login.html'), 400

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            flash('Invalid password format.', 'danger')
            return render_template('login.html'), 400

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid credentials. Please try again.', 'danger')
        return render_template('login.html'), 401

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            flash('Invalid username format.', 'danger')
            return render_template('register.html'), 400

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            flash('Invalid email format.', 'danger')
            return render_template('register.html'), 400

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            flash('Invalid password format.', 'danger')
            return render_template('register.html'), 400

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose another.', 'danger')
            return render_template('register.html'), 400

        new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Account deleted successfully. We\'re sorry to see you go.', 'info')
    return redirect(url_for('main.home'))