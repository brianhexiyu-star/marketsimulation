from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .model import MarketItem as Item
from .model import Market
from .model import User
from .init import db


market = Blueprint('market', __name__)

@market.route('/market')
def market_page():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=session['user']).first()
    markets = Market.query.all()
    items = Item.query.filter_by(market_id=None, buyer_email=None).all()
    prize = Item.prize

    return render_template(
        "market.html",
        markets=markets,
        items=items,
        prize=prize,
        points=user.points
    )

@market.route('/market/charge', methods=['POST'])
def charge_points():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    amount = request.form.get('amount', type=int)

    # Only allow fixed values
    if amount not in [10, 20, 50, 100]:
        flash("Invalid charge amount", "error")
        return redirect(url_for('market.market_page'))

    user = User.query.filter_by(email=session['user']).first()

    # Simulate successful payment
    user.points += amount
    db.session.commit()

    flash(f"Successfully charged RM{amount}. Points added!", "success")
    return redirect(url_for('market.market_page'))



@market.route('/market/purchase/<int:item_id>', methods=['POST'])
def purchase_item(item_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=session['user']).first()
    item = Item.query.get_or_404(item_id)


    if item.seller_email == user.email:
        flash("You cannot purchase your own item.", "error")
        return redirect(url_for('market.market_page'))
    
    if item.buyer_email is not None:
        flash("This item has already been purchased.", "error")
        return redirect(url_for('market.market_page'))

    # Check if user has enough points
    if user.points < item.prize:
        flash("You do not have enough points to purchase this item.", "error")
        return redirect(url_for('market.market_page'))

    # Deduct points
    user.points -= item.prize
    item.buyer_email = user.email
    db.session.commit()

    flash(f"You have successfully purchased '{item.title}'!", "success")
    return redirect(url_for('market.market_page'))