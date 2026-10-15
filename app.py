from flask import Flask, render_template, request
from database import db
from models import Transaction
from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import IntegrityError
import os
from threading import Barrier
import uuid
import math



app = Flask(__name__, template_folder="../frontend/templates")
test_barrier = Barrier(2)
@app.errorhandler(500)
def internal_server_error(error):
    return "Đả xảy ra lỗi. Vui lòng thử lại sau.", 500

app.config.from_object("config.Config")

db.init_app(app)


@app.route("/")
def home():
    return "CDE Lab Backend is running"


@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/transaction", methods=["GET", "POST"])
def transaction():
    transaction = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).all()

    return render_template("transactions.html", transactions=transaction)



@app.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        amount_raw = request.form.get("amount", "").strip()
        idempotency_key = request.form.get("idempotency_key", "").strip()   

        if not amount_raw:
            return "Invalid amount", 400
        try:
            amount = Decimal(amount_raw)
        except InvalidOperation:
            return "Invalid amount", 400

        if not amount.is_finite() or amount <= 0:
            return "Invalid amount", 400

        if amount.as_tuple().exponent < -2:
            return "Invalid amount", 400

        existing_transaction = Transaction.query.filter_by(
            idempotency_key=idempotency_key
        ).first()

        
        if existing_transaction:
            if existing_transaction.amount != amount:
                return "Idempotency key đả được sử dụng với số tiền khác.", 409

            return render_template(
                "result.html",
                transactions=existing_transaction
            )

        transaction = Transaction(
            amount=amount,
            transaction_ref=str(uuid.uuid4()),
            idempotency_key=idempotency_key
        )
        
        try:
            db.session.add(transaction)
            db.session.commit()
        except IntegrityError:
            app.logger.warning("Đả vào nhánh IntergrityError")
            db.session.rollback()

            existing_transaction = Transaction.query.filter_by(
                idempotency_key=idempotency_key
            ).first()

            if existing_transaction: 
                if existing_transaction.amount != amount:
                    return "Idempotemcy key đả được sử dụng với số tiền khác.", 409           
                   
                return render_template(
                    "result.html",
                    transactions=existing_transaction
                )
            raise
        except Exception:
            db.session.rollback()
            app.log_exception("Failed to save transaction")
            raise

        return render_template("result.html", transactions=transaction)
    
    
    
    return render_template("payment.html", idempotency_key=str(uuid.uuid4()))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
