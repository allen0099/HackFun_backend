from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from app.models import Tab, Course

edit = Blueprint("page", __name__)

query_return = {
    "SUCCESS": "Add query success!",
    "FAIL": "Add query failed!",

    "NULL": "String has nothing, check parameter!",
    "TOOLONG": "String tooooooo long!"
}


def check_length(string: str, limit: int = None) -> bool:
    if len(string) == 0:
        flash(query_return["NULL"], "fail")
        return False
    if limit is not None:
        if len(string) > limit:
            flash(query_return["TOOLONG"], "fail")
            return False
    return True


def not_in_db(query) -> bool:
    if query is not None:
        return False
    else:
        return True


@edit.route("/add_tab", methods=["POST"])
@login_required
def add_new_tab():
    _tab = request.values.get("tab")

    if check_length(_tab, 15):
        if not_in_db(Tab.query.filter_by(name=_tab).first()):
            db.session.add(Tab(name=_tab))
            db.session.commit()
            flash(query_return["SUCCESS"], "success")
        else:
            flash(query_return["FAIL"], "fail")
    return redirect(url_for("page.edit_page"))


@edit.route("/add_course", methods=["POST"])
@login_required
def add_new_course():
    _tab = request.values.get("tab")
    _name = request.values.get("name")
    _desc = request.values.get("description")

    if check_length(_tab, 15):
        if not not_in_db(Tab.query.filter_by(name=_tab).first()):
            if check_length(_name, 50) and check_length(_desc):
                db.session.add(Course(belong=_tab, name=_name, description=_desc))
                db.session.commit()
                flash(query_return["SUCCESS"], "success")
        else:
            flash(query_return["FAIL"], "fail")
    return redirect(url_for("page.edit_page"))


@edit.route("/edit")
@login_required
def edit_page():
    print(current_user)
    if current_user.id in ["113635293585592202061", "109728865859768459887", "103073582772399260317"]:
        tabs = Tab.query.order_by(Tab.name).all()
        course = Course.query.order_by(Course.name).all()
        return render_template("edit.html", tabs=tabs, courses=course)
    else:
        return redirect(url_for("login.index"))
