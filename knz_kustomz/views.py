from datetime import timedelta

import pandas as pd

# import requests
# import sqlalchemy as sa
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash

from knz_kustomz import app, db
from knz_kustomz.forms import LocationsForm, LoginForm, PaysheetsForm, RegistrationForm
from knz_kustomz.helpers import add_location, create_user, get_location, usd
from knz_kustomz.models import Locations, Paysheets, User

# Colors for flashed messages
success = "green accent-1"
failure = "red accent-1"

# Filter for USD display
app.jinja_env.filters["usd"] = usd


# Index route with paysheet display
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    data = Paysheets.query.filter_by(user_id=current_user.id).all()
    if data:
        df = pd.DataFrame(
            [
                (
                    d.id,
                    d.user_id,
                    d.date,
                    d.starting_milage,
                    d.ending_milage,
                    d.total_miles,
                    d.backhaul,
                    d.truck,
                    d.delay,
                )
                for d in data
            ],
            columns=[
                "id",
                "user_id",
                "date",
                "starting milage",
                "ending milage",
                "total miles",
                "backhaul",
                "truck",
                "delay",
            ],
        )
        df["date"] = pd.to_datetime(df["date"])
        df.set_index(df["date"], inplace=True)
        now = df["date"].max()
        # now = now + timedelta(days=1)
        first = df["date"].min()
        first = first - timedelta(days=1)
        rng = pd.date_range(start=first, end=now, freq="W")
        week_starting = [pd.to_datetime(rng[x]) for x in range(len(rng))]

        def get_weekly(week_starting, week_ending, df):
            filtered_df = df.loc[
                (df["date"] >= week_starting) & (df["date"] < week_ending)
            ]
            total_miles = int(filtered_df["total miles"].sum())
            total_backhaul = filtered_df["backhaul"].sum()
            pay_miles = round(total_miles * 0.505, 2)
            delay = (filtered_df["delay"].sum()) * 13.25
            total = pay_miles + total_backhaul + delay
            week_starting = pd.to_datetime(week_starting)
            return (week_starting, total_miles, pay_miles, total_backhaul, total, delay)

        totals_list = []
        for x in range(len(rng)):
            week_ending = pd.to_datetime(week_starting[x] + timedelta(days=7))
            totals_list.append(get_weekly(week_starting[x], week_ending, df))
        #     print(f"  WEEKSTARTING{week_starting}  WEEKENDING{week_ending}")
        # print(
        #     f"Total List {totals_list} DATA{data}  NOW{now}  FIRST{first} RNG{rng} DF{df}"
        # )
        length = len(totals_list)
        entries = True

        return render_template(
            "index.html",
            title="Welcome",
            logged_in=current_user.is_authenticated,
            length=length,
            totals_list=totals_list,
            entries=entries,
        )
    else:
        return render_template(
            "index.html", title="Welcome", logged_in=current_user.is_authenticated
        )


# Weekly paysheet route
@app.route("/week/<week>", methods=["GET", "POST"])
@login_required
def week(week):
    starting = pd.to_datetime(week, format="%Y-%m-%d")
    ending = starting + timedelta(days=7)
    data = Paysheets.query.filter(Paysheets.date.between(starting, ending)).all()
    length = len(data)
    return render_template(
        "week.html",
        title="Week",
        logged_in=current_user.is_authenticated,
        data=data,
        length=length,
    )


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        user = User.get_user(form.email.data)
        if not check_password_hash(user.password, form.password.data):
            flash("Password or email don't match please try again", failure)
            return render_template("login.html", title="Login", form=form)
        else:
            remember = form.remember.data
            login_user(user, remember=remember)
            return redirect(url_for("index"))

    else:
        return render_template(
            "login.html",
            title="Login",
            form=form,
            logged_in=current_user.is_authenticated,
        )


# Logout route
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Registration route
@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        create_user(email, password)
        flash(f"Account created for {email}", success)
        return redirect(url_for("login"))
    else:
        return render_template(
            "registerFF.html",
            title="Register",
            form=form,
            logged_in=current_user.is_authenticated,
        )


# Paysheets route
@app.route("/paysheets", methods=["POST", "GET"])
@login_required
def paysheets():
    form = PaysheetsForm()

    if request.method == "POST":
        if form.validate_on_submit:

            user_id = current_user.id
            date_obj = form.date.data
            sheet = Paysheets.query.filter(
                (Paysheets.user_id == user_id) & (Paysheets.date == date_obj)
            ).first()
            if sheet == None:

                sheet = Paysheets(
                    user_id=current_user.id,
                    truck=form.truck.data,
                    date=form.date.data,
                    starting_milage=form.starting_milage.data,
                    ending_milage=form.ending_milage.data,
                    total_miles=form.miles.data,
                    backhaul=form.backhaul.data,
                    delay=form.delay.data,
                )
                db.session.add(sheet)
                db.session.commit()
                return redirect(url_for("index"))

            else:
                if form.miles.data:
                    sheet.total_miles = form.miles.data
                if form.backhaul.data:
                    sheet.backhaul = form.backhaul.data
                if form.ending_milage.data:
                    sheet.ending_milage = form.ending_milage.data
                if form.starting_milage.data:
                    sheet.starting_milage = form.starting_milage.data
                if form.truck.data:
                    sheet.truck = form.truck.data
                if form.delay.data:
                    sheet.delay = form.delay.data
                db.session.commit()
                return redirect(url_for("index"))

    return render_template(
        "paysheets.html",
        title="Paysheets",
        form=form,
        logged_in=current_user.is_authenticated,
    )


# Locations choice route
@app.route("/locations", methods=["POST", "GET"])
@login_required
def locations():

    locations = Locations.query.all()
    form = LocationsForm()
    form.locations.choices = [l.name for l in locations]
    if request.method == "POST":
        if form.validate_on_submit:
            return redirect(url_for("location", location=form.locations.data))
    return render_template(
        "locations.html",
        title="Locations",
        form=form,
        logged_in=current_user.is_authenticated,
    )


# Single location route with maps
@app.route("/location/<location>", methods=["POST", "GET"])
@login_required
def location(location):
    place = Locations.query.filter_by(name=location).first()
    tulsa = Locations.query.filter_by(name="Tulsa").first()
    api_key = app.config.get("GOOGLE_API_KEY")
    print(place.place_id, tulsa.place_id)
    return render_template(
        "location.html",
        title=location,
        logged_in=current_user.is_authenticated,
        place=place,
        tulsa=tulsa,
    )


@app.errorhandler(404)
def error_404(err):
    return render_template("error_404.html", err=err), 404


@app.errorhandler(403)
def error_404(err):
    return render_template("error_403.html", err=err), 403


@app.errorhandler(500)
def error_404(err):
    return render_template("error_500.html", err=err), 500
