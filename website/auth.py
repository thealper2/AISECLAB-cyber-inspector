from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.dashboard"))

            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email not found. Please sign up!", category="error")

    return render_template("login_and_signup.html", user=current_user)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists.", category="error")
        elif len(username) < 4:
            flash("Username must be greater than 4 characters.", category="error")
        elif password1 != password2:
            flash("Passwords dont match.", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters.", category="error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.dashboard"))

    return render_template("login_and_signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
