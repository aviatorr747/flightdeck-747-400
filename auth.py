import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from . import db
from .models import User

auth_bp = Blueprint("auth", __name__)

def valid_email(email):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or ""))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.explore"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", username):
            errors.append("Username must be 3–30 characters using letters, numbers or underscores.")
        if not valid_email(email) or len(email) > 254:
            errors.append("Enter a valid email address.")
        if len(password) < 12:
            errors.append("Password must be at least 12 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if User.query.filter(or_(User.username == username, User.email == email)).first():
            errors.append("That username or email is already registered.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("register.html")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Your account is ready. Welcome aboard!", "success")
        return redirect(url_for("main.explore"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.explore"))
    if request.method == "POST":
        identity = request.form.get("identity", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter(
            or_(User.username == identity, User.email == identity.lower())
        ).first()
        if user and user.check_password(password):
            login_user(user, remember=False)
            flash("Signed in successfully.", "success")
            next_url = request.args.get("next", "")
            # Only allow local relative paths to avoid open redirects.
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect(url_for("main.explore"))
        flash("The sign-in details were not recognised.", "error")
    return render_template("login.html")

@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("main.index"))
