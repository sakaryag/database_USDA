from datetime import datetime
from food import food_group
from food import food_detail
from flask import flash

import sqlite3

from flask import current_app, render_template,request,redirect, url_for
from flask_login import login_required
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


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
