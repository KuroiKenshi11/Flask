#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Project import weather_data
from Project.model import User
from Project.forms import Login, Register, TempretureSearch
from Project import app, db
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from urllib.error import HTTPError


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        try:
            form = TempretureSearch()
            search = form.search.data
            weather = weather_data.get_weatherData(
                city=search, api_key="d787b14cd78be94197b35c82f2a06419")
            cityName = weather["name"]
            temp = str("{:.1f}").format((int(weather["main"]["temp"]) - 273))
            return render_template("index.html", form=form, city=cityName, temp=temp)
        except HTTPError:
            return render_template("errors/HTTPError.html")
    else:
        flash("First, You should Log in and then you can start!")
        return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if (form.validate_on_submit()):
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
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


if __name__ == "__main__":
    app.run(debug=True)
