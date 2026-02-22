from flask import request, redirect, url_for
from flask_login import login_user, logout_user
from app.extensions import db
from app.models.user import User
from . import auth_bp

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            return "User already exists"

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("dashboard.home"))

    return """
    <form method="POST">
        <input name="email" placeholder="Email">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Register</button>
    </form>
    """

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard.home"))

        return "Invalid credentials"

    return """
    <form method="POST">
        <input name="email" placeholder="Email">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    """

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))