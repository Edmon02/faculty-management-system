# app/routes/auth.py
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)


# Define login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "logged_in" in session:
        return redirect(url_for("dashboard.dashboard"))
    return render_template("index.html")


@auth_bp.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    auth_controller = AuthController()

    validate = bool(form.username.data and form.password.data)
    if request.method == "POST" and validate:
        username, password = form.username.data, form.password.data
        result, status_code = auth_controller.authenticate(username, password, request.remote_addr)

        if status_code == 200:
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": result["message"]}), status_code

    return render_template("index.html", form=form)


@auth_bp.route("/logout")
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page
    return redirect(url_for("auth.index"))
