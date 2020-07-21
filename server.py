from flask import Flask
from flask_login import LoginManager
from user import get_user

import views
import os

from database import Database
from food import food_group
from food import food_detail


lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/foods/<int:food_key>", view_func=views.food_page)


    lm.init_app(app)
    lm.login_view = "login_page"

    app.add_url_rule(
        "/foods", view_func=views.food_group_page, methods=["GET", "POST"]
        )
    app.add_url_rule(
        "/login", view_func=views.login_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/logout", view_func=views.logout_page)


    app.add_url_rule("/foods/<int:food_key>", view_func=views.food_page)

    app.add_url_rule(
        "/foods/<int:food_key>/edit",
        view_func=views.food_edit_page,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/new-food", view_func=views.food_add_page, methods=["GET", "POST"]
    )

    home_dir = os.path.expanduser("~")
    db = Database(os.path.join(home_dir, "food.db"))
    app.config["db"] = db

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
