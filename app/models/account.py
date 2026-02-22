from datetime import datetime
from app.extensions import db

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    name = db.Column(db.String(80), nullable=False)
    institution = db.Column(db.String(80), nullable=True)

    type = db.Column(db.String(20), nullable=False)  
    # checking | savings | cash | credit

    opening_balance_pennies = db.Column(db.BigInteger, nullable=False, default=0)

    # Only for credit cards
    credit_limit_pennies = db.Column(db.BigInteger, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "name", name="uq_user_account_name"),
    )

    def __repr__(self):
        return f"<Account {self.name}>"