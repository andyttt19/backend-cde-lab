from database import db
from datetime import datetime, timezone

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False, default="pending")
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_ref = db.Column(db.String(36), unique=True, nullable=False)
    idempotency_key = db.Column(db.String(64), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
