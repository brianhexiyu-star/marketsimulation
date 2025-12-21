from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .model import User
import re
from .init import db

from sqlalchemy.exc import IntegrityError


auth = Blueprint('auth', __name__)


#validation function for email
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not is_valid_email(email):
            flash('Invalid email format.', 'error')
            
            return redirect(url_for('auth.login'))
            

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.email
            session['is_premium'] = user.is_premium
            return redirect(url_for('views.dashboard'))

        flash('Incorrect email or password.', 'error')
        return redirect(url_for('auth.login'))
        

    return render_template('login.html')




@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('views.home'))




@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        

        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'error')
            
            return redirect(url_for('auth.signup'))

        new_user = User(
            email=email,
            password= generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)  
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            user = User.query.filter_by(email=email).first()
            session['user'] = new_user.email
            session['is_premium'] = user.is_premium
            return redirect(url_for('views.dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash("Email already registered.", "error")
            return redirect(url_for('auth.signup'))

        

    return render_template('signup.html')

