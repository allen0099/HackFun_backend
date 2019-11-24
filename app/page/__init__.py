from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from app.models import Tab, Course

edit = Blueprint("page", __name__)


@edit.route("/add_tab", methods=["POST"])
@login_required
def add_new_page():
    _tab = request.values.get("tab")

    _check = Tab.query.filter_by(name=_tab).first()
    if _tab == "":
        flash("Check parameters!", "fail")
    elif len(_tab) > 15:
        flash("Check length!", "fail")
    else:
        if _check is None:
            db.session.add(Tab(name=_tab))
            db.session.commit()
            flash("Add success!", "success")
        else:
            flash("Add fail!", "fail")
    return redirect(url_for("page.edit_page"))


@edit.route("/add_course", methods=["POST"])
@login_required
def add_new_course():
    _tab = request.values.get("tab")
    _name = request.values.get("name")
    _desc = request.values.get("description")

    _check = Course.query.filter_by(name=_name).first()
    if (_tab and _name and _desc) == "":
        flash("Check parameters!", "fail")
    else:
        if _check is None:
            # db.session.add(Course(name=_name, description=_desc))
            # db.session.commit()
            flash("Add success!", "success")
        else:
            flash("Add fail!", "fail")
    return redirect(url_for("page.edit_page"))


@edit.route("/edit")
@login_required
def edit_page():
    print(current_user)
    if current_user.id == ("109728865859768459887" or "113635293585592202061" or "103073582772399260317"):
        tabs = Tab.query.order_by(Tab.name).all()
        return render_template("edit.html", tabs=tabs)
    else:
        return redirect(url_for("login.index"))
