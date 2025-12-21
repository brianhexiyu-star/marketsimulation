from flask import Blueprint, render_template, session, redirect, url_for, flash
from .model import User as user
from .init import db

premium = Blueprint('premium', __name__)


@premium.route('/subscribe')
def subscribe_page():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    
    return render_template('premium.html', is_premium=session['is_premium'])


@premium.route('/subscribe/confirm', methods=['POST'])
def confirm_subscription():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Simulate successful payment
    if session['is_premium']:
        flash("You are already a Premium user!", "info")
        return redirect(url_for('account.account_page'))
    user.is_premium = True
    db.session.commit()
    session['is_premium'] = True

    flash("You are now a Premium user!", "success")
    return redirect(url_for('account.account_page'))