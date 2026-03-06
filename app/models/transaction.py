from datetime import datetime, date
from app.extensions import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)

    date = db.Column(db.Date, nullable=False, default=date.today)

    type = db.Column(db.String(10), nullable=False)  
    # income | expense | transfer

    amount_pennies = db.Column(db.BigInteger, nullable=False)

    description = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship("Account")