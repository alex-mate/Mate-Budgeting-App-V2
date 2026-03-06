from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.account import Account
from . import accounts_bp

@accounts_bp.route("/")
@login_required
def list_accounts():
    accounts = Account.query.filter_by(user_id=current_user.id).order_by(Account.created_at.desc()).all()
    return render_template("accounts/list.html", accounts=accounts)

@accounts_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_account():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        institution = request.form.get("institution", "").strip() or None
        acc_type = request.form.get("type", "").strip()
        opening_balance = request.form.get("opening_balance", "0").strip()
        credit_limit = request.form.get("credit_limit", "").strip()

        if not name:
            flash("Account name is required.", "error")
            return redirect(url_for("accounts.new_account"))

        if acc_type not in {"checking", "savings", "cash", "credit"}:
            flash("Invalid account type.", "error")
            return redirect(url_for("accounts.new_account"))

        try:
            opening_pennies = int(round(float(opening_balance) * 100))
        except ValueError:
            flash("Opening balance must be a number.", "error")
            return redirect(url_for("accounts.new_account"))

        credit_limit_pennies = None
        if acc_type == "credit":
            if not credit_limit:
                flash("Credit limit is required for credit accounts.", "error")
                return redirect(url_for("accounts.new_account"))
            try:
                credit_limit_pennies = int(round(float(credit_limit) * 100))
            except ValueError:
                flash("Credit limit must be a number.", "error")
                return redirect(url_for("accounts.new_account"))

        account = Account(
            user_id=current_user.id,
            name=name,
            institution=institution,
            type=acc_type,
            opening_balance_pennies=opening_pennies,
            credit_limit_pennies=credit_limit_pennies
        )

        db.session.add(account)
        db.session.commit()

        flash("Account created.", "success")
        return redirect(url_for("accounts.list_accounts"))

    return render_template("accounts/new.html")