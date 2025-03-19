from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user
from models import User, db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")
