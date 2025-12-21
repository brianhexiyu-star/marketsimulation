from .init import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.email}>'

class Market(db.Model):
    __tablename__ = "markets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_email = db.Column(db.String(120), nullable=False)

class MarketItem(db.Model):
    __tablename__ = "market_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    prize = db.Column(db.Integer, nullable=False)

    seller_email = db.Column(db.String(120), nullable=False)
    buyer_email = db.Column(db.String(120), nullable=True)

    market_id = db.Column(db.Integer, nullable=True)
