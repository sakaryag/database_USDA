from datetime import datetime
from food import food_group
from food import food_detail
from flask import flash
from forms import LoginForm
from user import User
from user import get_user
from flask_login import login_user, logout_user,current_user
from passlib.hash import pbkdf2_sha256 as hasher
import sqlite3

from flask import current_app, render_template,request,redirect, url_for
from flask_login import login_required
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

@login_required
def food_add_page():
    if not current_user.is_admin:
        abort(401)
    if request.method == "GET":
        values = {"title": ""}
        return render_template(
            "food_edit.html",
            values=values,
        )
    else:
        valid = validate_food_form(request.form)
        if not valid:
            return render_template(
                "food_edit.html",
                values=request.form,
            )
        title = request.form["title"]
        foods = food_group(title)
        db = current_app.config["db"]
        foods_key = db.add_food(foods)
        return redirect(url_for("food_page", foods_key=foods_key))
def food_group_add_page():
    if not current_user.is_admin:
        abort(401)
    if request.method == "GET":
        values = {"title": ""}
        return render_template(
            "food_group_edit.html",
            values=values,
        )
    else:
        valid = validate_food_form(request.form)
        if not valid:
            return render_template(
                "food_group_edit.html",
                values=request.form,
            )
        title = request.form["title"]
        foods = food_group(title)
        db = current_app.config["db"]
        foods_key = db.add_food_group(foods)
        return redirect(url_for("food_group_page", foods_key=foods_key))

@login_required
def food_edit_page(food_key):
    if request.method == "GET":
        db = current_app.config["db"]
        foods = db.get_food()
        if foods is None:
            abort(404)
        values = {"title": food_details.title}
        return render_template(
            "food_group_edit.html",
            values=values,
        )
    else:
        valid = validate_food_form(request.form)
        if not valid:
            return render_template(
                "food_group_edit.html",
                values=request.form,
            )
        title = request.form.data["title"]
        foods = food_group(title)
        db = current_app.config["db"]
        db.update_food(food_key, foods)
        return redirect(url_for("food_page", food_key=food_key))
def validate_food_form(form):
    form.data = {}
    form.errors = {}

    form_title = form.get("title", "").strip()
    if len(form_title) == 0:
        form.errors["title"] = "Title can not be blank."
    else:
        form.data["title"] = form_title

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

def food_group_page():
    db = current_app.config["db"]
    if request.method == "GET":
        foods = db.get_food_group()
        return render_template("foods.html", foods=sorted(foods))
    else:
        if not current_user.is_admin:
            abort(401)
        form_food_keys = request.form.getlist("food_keys")
        for form_food_key in form_food_keys:
            db.delete_food(int(form_food_key))
        flash("%(num)d foods deleted." % {"num": len(form_food_keys)})
        return redirect(url_for("food_group_page"))
def food_page(food_key):
    db = current_app.config["db"]
    food= db.get_food()
    return render_template("food.html", food_detail=food)
