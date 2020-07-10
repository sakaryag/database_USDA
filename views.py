from datetime import datetime
from earthquake import Earthquake
from flask import flash
from forms import LoginForm
from user import User
from user import get_user
from flask_login import login_user, logout_user,current_user
from passlib.hash import pbkdf2_sha256 as hasher

from flask import current_app, render_template,request,redirect, url_for
from flask_login import login_required
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def earthquakes_page():
    db = current_app.config["db"]
    if request.method == "GET":
        earthquakes = db.get_earthquakes()
        return render_template("earthquakes.html", earthquakes=sorted(earthquakes))
    else:
        if not current_user.is_admin:
            abort(401)
        form_earthquake_keys = request.form.getlist("earthquake_keys")
        for form_earthquake_key in form_earthquake_keys:
            db.delete_earthquake(int(form_earthquake_key))
        return redirect(url_for("earthquakes_page"))

def earthquake_page(earthquake_key):
    db = current_app.config["db"]
    earthquake = db.get_earthquake(earthquake_key)
    return render_template("earthquake.html", earthquake=earthquake)

@login_required
def earthquake_add_page():
    if not current_user.is_admin:
        abort(401)
    if request.method == "GET":
        values = {"title": "", "year": ""}
        return render_template(
            "earthquake_edit.html",
            min_year=1887,
            max_year=datetime.now().year,
            values=values,
        )
    else:
        valid = validate_earthquake_form(request.form)
        if not valid:
            return render_template(
                "earthquake_edit.html",
                min_year=1887,
                max_year=datetime.now().year,
                values=request.form,
            )
        title = request.form["title"]
        year = request.form["year"]
        earthquake = Earthquake(title, year=int(year) if year else None)
        db = current_app.config["db"]
        earthquakes_key = db.add_earthquake(earthquake)
        return redirect(url_for("earthquakes_page", earthquakes_key=earthquakes_key))

@login_required
def earthquake_edit_page(earthquake_key):
    if request.method == "GET":
        db = current_app.config["db"]
        earthquake = db.get_earthquake(earthquake_key)
        if earthquake is None:
            abort(404)
        values = {"title": earthquake.title, "year": earthquake.year}
        return render_template(
            "earthquake_edit.html",
            min_year=1887,
            max_year=datetime.now().year,
            values=values,
        )
    else:
        valid = validate_earthquake_form(request.form)
        if not valid:
            return render_template(
                "earthquake_edit.html",
                min_year=1887,
                max_year=datetime.now().year,
                values=request.form,
            )
        title = request.form.data["title"]
        year = request.form.data["year"]
        earthquake = earthquake(title, year=year)
        db = current_app.config["db"]
        db.update_earthquake(earthquake_key, earthquake)
        return redirect(url_for("earthquake_page", earthquake_key=earthquake_key))
def validate_earthquake_form(form):
    form.data = {}
    form.errors = {}

    form_title = form.get("title", "").strip()
    if len(form_title) == 0:
        form.errors["title"] = "Title can not be blank."
    else:
        form.data["title"] = form_title

    form_year = form.get("year")
    if not form_year:
        form.data["year"] = None
    elif not form_year.isdigit():
        form.errors["year"] = "Year must consist of digits only."
    else:
        year = int(form_year)
        if (year < 1887) or (year > datetime.now().year):
            form.errors["year"] = "Year not in valid range."
        else:
            form.data["year"] = year

    return len(form.errors) == 0

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))
