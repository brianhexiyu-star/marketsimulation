from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from .model import MarketItem as Item
from .model import Market as Market
from .init import db

account = Blueprint('account', __name__)

@account.route('/account')
def account_page():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user_email = session['user']
    items = Item.query.filter_by(seller_email=user_email).all()
    markets = Market.query.filter_by(owner_email=user_email).all()
    bought_items = Item.query.filter_by(buyer_email=user_email).all()

    prize = Item.prize


    return render_template(
        'account.html',
        email=user_email,
        items=items,
        markets=markets,
        prize = prize,
        is_premium=session['is_premium'],
        bought_items=bought_items
    )


@account.route('/account/add-item', methods=['POST'])
def add_item():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    description = request.form.get('description')
    prize = request.form.get('prize', type=int)

    if not title or not description:
        flash("Title and description are required", "error")
        return redirect(url_for('account.account_page'))

    new_item = Item(
        title=title,
        description=description,
        seller_email=session['user'],
        prize=prize
    )

    db.session.add(new_item)
    db.session.commit()

    flash("Item added successfully", "success")
    return redirect(url_for('account.account_page'))

@account.route('/account/delete-item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    item = Item.query.get_or_404(item_id)

    # 🔐 ownership check
    if item.seller_email != session['user']:
        flash("Unauthorized action", "error")
        return redirect(url_for('account.account_page'))
    
    if item.buyer_email is not None:
        flash("Cannot delete an item that has been purchased", "error")
        return redirect(url_for('account.account_page'))

    db.session.delete(item)
    db.session.commit()

    flash("Item deleted", "success")
    return redirect(url_for('account.account_page'))


@account.route('/account/create-market', methods=['POST'])
def create_market():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if not session['is_premium']:
        flash("Upgrade to Premium to create markets!", "error")
        return redirect(url_for('account.account_page'))

    name = request.form.get('market_name')

    if not name:
        flash("Market name required", "error")
        return redirect(url_for('account.account_page'))

    market = Market(
        name=name,
        owner_email=session['user']
    )

    db.session.add(market)
    db.session.commit()

    flash("Market created!", "success")
    return redirect(url_for('account.account_page'))





@account.route('/account/add-market-item', methods=['POST'])
def add_market_item():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if not session['is_premium']:
        flash("Upgrade to Premium to add market items!", "error")
        return redirect(url_for('account.account_page'))

    title = request.form.get('title')
    description = request.form.get('description')
    market_id = request.form.get('market_id')
    prize = request.form.get('prize', type=int)
    

    if not title or not description:
        flash("All fields required", "error")
        return redirect(url_for('account.account_page'))

    item = Item(
        title=title,
        description=description,
        seller_email=session['user'],
        market_id=market_id,
        prize=prize
    )

    db.session.add(item)
    db.session.commit()

    flash("Item added to market", "success")
    return redirect(url_for('account.account_page'))
