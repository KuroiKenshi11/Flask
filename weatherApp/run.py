#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Project import weather_data  # take weather info
from Project.model import User  # save user in database
from Project.forms import Login, Register, TempretureSearch  # check user data
from Project import app, db  # import app and db to run the app
# handle pages and requests
from flask import render_template, redirect, url_for, request, flash
# login methods and functionss
from flask_login import login_user, logout_user, login_required, current_user
from urllib.error import HTTPError  # if their is an HTTPError
from http.client import InvalidURL  # if their is and InvalidURL
from werkzeug.exceptions import BadRequest  # if their is bad request error


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    This is home page where user can search for the country and get the weather info. 
    and it required user to log in otherwise user can't access this page.
    """
    # if current_user.is_authenticated:
    try:
        form = TempretureSearch()
        search = str(form.search.data).strip()
        weather = weather_data.get_weatherData(
            search, api_key="d787b14cd78be94197b35c82f2a06419")
        name = weather["city_name"]
        country_code = weather["country_code"]
        main = weather["main_weather"]
        desc = weather["description"]
        temp = weather["temp"]
        min_temp = weather["temp_min"]
        max_temp = weather["temp_max"]
        coord_lon = weather["coord_lon"]
        coord_lat = weather["coord_lat"]

        return render_template("index.html", title="Home",  form=form,
                               name=name, country_code=country_code,
                               main=main, desc=desc, temp=temp,
                               min_temp=min_temp, max_temp=max_temp,
                               coord_lon=coord_lon, coord_lat=coord_lat)
    except HTTPError:
        return render_template("errors/HTTPError.html")
    except InvalidURL:
        return render_template("errors/HTTPInvalidurl.html")
    # else:
    #     flash("Please Log in to access Home page.")
    #     return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register view to handle the registration page for users.   
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = Register()
    if (form.validate_on_submit()):
        if form.check_username(form.username.data) or form.check_email(form.email.data):
            flash("Your email or username is already exist!")
            return redirect(url_for("register"))
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login view to handle the log in page for users.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = Login()
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Thanks for Logging In!")
            next = request.args.get("next")
            if next is None or not next[0] == "/":
                next = url_for("index")
            return redirect(next)
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
@login_required
def logout():
    """
    A view to make user log out, with logout_user function.
    """
    logout_user()
    return redirect(url_for("index"))


# An error vews to handle error pages
@app.errorhandler(404)
def handle_error_404(e):
    return render_template("errors/404.html", title="Error"), 404


@app.errorhandler(405)
def handle_error_405(e):
    return render_template("errors/405.html", title="Error"), 405


@app.errorhandler(BadRequest)
def handle_error_400(e):
    return render_template("errors/400.html", title="Error"), 400


@app.before_first_request
def create_table():
    """
    Create a database before any requests.
    """
    return db.create_all()


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
