from flask import (render_template, Blueprint, flash, request, redirect, url_for)
from flask_login import (login_required, current_user)
from models import db
from models.trek import Trek
from models.user import User
from models.booking import Booking

staff_bp = Blueprint("staff",__name__,url_prefix= "/staff")

def is_staff():
    return current_user.is_authenticated and current_user.role == "staff" and current_user.approved and not current_user.blacklisted

@staff_bp.route("/dashboard")
@login_required
def staff_dashboard():
    if not is_staff:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("auth.signin"))
    assigned_treks = db.session.query(Trek).filter_by(assigned_staff_id = current_user.user_id).all()
    return render_template("staff/staff_dashboard.html", treks = assigned_treks)

@staff_bp.route("/booked_treks/<int:trek_id>")
def booked_treks(trek_id):
    if not is_staff():
        flash("Unauthorized Access", "danger")
        return redirect(url_for("auth.signin"))
    trek = db.session.query(Trek).get_or_404(trek_id)
    if trek.assigned_staff_id != current_user.user_id:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("staff.staff_dashboard"))

    booking = db.session.query(Booking).filter_by(trek_id = trek_id).all()
    return render_template("staff/booked_treks.html", trek = trek, bookings = booking)

@staff_bp.route("/update_trek/<int:trek_id>", methods = ["GET", "POST"])
def update_trek(trek_id):
    if not is_staff():
        flash("Unauthorized Access", "danger")
        return redirect(url_for("auth.signin"))
    trek = db.session.query(Trek).get_or_404(trek_id)
    if trek.assigned_staff_id != current_user.user_id:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("staff.staff_dashboard"))

    if request.method == "POST":
        trek.available_slots = int(request.form["available_slots"])
        trek.status = request.form["status"]
        db.session.commit()
        flash("Trek Details Updated!", "success")
        return redirect(url_for("staff.staff_dashboard"))
    return render_template("staff/update_trek.html", trek = trek)
