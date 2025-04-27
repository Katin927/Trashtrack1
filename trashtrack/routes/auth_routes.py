from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required
from models import User, db

auth_bp = Blueprint("auth", __name__)

# ✅ Login Route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("auth/login.html")

# ✅ Signup Route
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")  # ✅ now captured
        password = request.form.get("password")

        # Validate form data
        if not username or not email or not password:
            flash("All fields are required.", "warning")
            return redirect(url_for("auth.signup"))

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash("Username already taken", "warning")
            return redirect(url_for("auth.signup"))
        if User.query.filter_by(email=email).first():
            flash("Email already in use", "warning")
            return redirect(url_for("auth.signup"))

        # Create and save new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("auth/signup.html")

# ✅ Logout Route
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for("auth.login"))
