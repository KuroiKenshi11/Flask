#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Project import weather_data
from Project.model import User
from Project.forms import Login, Register, TempretureSearch
from Project import app, db
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from urllib.error import HTTPError
from http.client import InvalidURL
from werkzeug.exceptions import BadRequest


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # if current_user.is_authenticated:
    try:
        form = TempretureSearch()
        search = str(form.search.data).strip()
        weather = weather_data.get_weatherData(
            search, api_key="d787b14cd78be94197b35c82f2a06419")
        name = weather["city_name"]
        temp = weather["temp"]
        min_temp = weather["temp_min"]
        max_temp = weather["temp_max"]

        return render_template("index.html", form=form,
                               name=name, temp=temp, min_temp=min_temp,
                               max_temp=max_temp)
    except HTTPError:
        return render_template("errors/HTTPError.html")
    except InvalidURL:
        return render_template("errors/HTTPInvalidurl.html")
    # else:
    #     flash("Please Log in to access Home page.")
    #     return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = Register()
    if (form.validate_on_submit()):
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = Login()
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get("next")
            if next is None or not next[0] == "/":
                next = url_for("index")
            return redirect(next)
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.errorhandler(404)
def handle_error_404(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(405)
def handle_error_405(e):
    return render_template("errors/405.html"), 405


@app.errorhandler(BadRequest)
def handle_error_400(e):
    return render_template("errors/400.html"), 400


@app.before_first_request
def create_table():
    return db.create_all()


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
