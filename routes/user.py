from flask import (render_template, request, redirect, url_for, Blueprint, flash)
from flask_login import (login_required, current_user)
from models import db
from models.trek import Trek
from models.user import User
from models.booking import Booking

user_bp = Blueprint("user",__name__,url_prefix= "/user")

def is_user():
    return current_user.role == "user" and current_user.is_authenticated

@user_bp.route("/dashboard")
@login_required
def user_dashboard():
    if not is_user():
        flash("Unauthorized Access", "danger")
        return redirect("/")

    open_treks = db.session.query(Trek).filter_by(status="open").all()

    return render_template("user/user_dashboard.html",treks= open_treks)

@user_bp.route("/show_profile")
@login_required
def show_profile():
    if not is_user():
        flash("Unauthorized Access", "danger")
        return redirect("/")
    profile = User.query.get_or_404(current_user.user_id)
    return render_template("user/show_profile.html", profile=profile, method= request.method)

@user_bp.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile():
    if not is_user():
        flash("Unauthorized Access", "danger")
        return redirect("/")
    profile = User.query.get_or_404(current_user.user_id)
    if request.method == "POST":
        profile.username = request.form["username"]
        profile.contact_no = request.form["contact_no"]
        profile.full_name = request.form["full_name"]
        profile.email = request.form["email"]
        db.session.commit()
        flash("Profile Updated", "success")
        return redirect(url_for("user.show_profile"))
    return render_template("user/update_profile.html", profile=profile, method= request.method)

@user_bp.route("/delete_profile")
@login_required
def delete_profile():
    if not is_user():
        flash("Unauthorized Access", "danger")
        return redirect("/")
    profile = User.query.get_or_404(current_user.user_id)
    db.session.delete(profile)
    db.session.commit()
    flash("Profile Deleted", "success")
    return redirect("/")

@user_bp.route("/my_bookings")
@login_required
def my_bookings():
    if not is_user():
        flash("Unauthorized Access", "danger")
        return redirect("/")
    bookings = Booking.query.filter_by(user_id=current_user.user_id).filter( Booking.trek.has(Trek.status =="open"), Booking.status == "booked").all()
    return render_template("user/my_bookings.html", bookings=bookings)

@user_bp.route("/book_trek/<int:trek_id>")
@login_required
def book_trek(trek_id):
    if not is_user():
        flash("Unauthorized Access", "danger")
        return redirect("/")
    trek = Trek.query.get_or_404(trek_id)
    if trek.status != "open":
        flash("Trek Not Available Currently", "danger")
        return redirect(url_for("user.user_dashboard"))
    if trek.available_slots <= 0:
        flash("No Slots Available", "danger")
        return redirect(url_for("user.user_dashboard"))

    already_booked = db.session.query(Booking).filter_by(user_id=current_user.user_id, trek_id=trek_id).first()
    if already_booked:
        flash("Already Booked", "danger")
        return redirect(url_for("user.user_dashboard"))
    booking = Booking(user_id=current_user.user_id, trek_id= trek_id)
    db.session.add(booking)
    trek.available_slots -= 1
    db.session.commit()
    flash("Trek Booked", "success")
    return redirect(url_for("user.user_dashboard"))

@user_bp.route("/cancel_booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    if not is_user():
        flash('Unauthorized Access!','danger')
        return redirect(url_for("/"))
    booking = db.session.query(Booking).filter_by(booking_id= booking_id).update({"status": "cancelled"})
    db.session.query(Trek).filter(Trek.bookings.any(booking_id=booking_id)).update({"available_slots": Trek.available_slots + 1})
    db.session.commit()
    flash("Booking Cancelled", "danger")
    return redirect(url_for("user.my_bookings"))

@user_bp.route("/my_history")
@login_required
def my_history():
    if not is_user():
        flash("Unauthorized Access", "danger")
        return redirect("/")
    history = Booking.query.filter_by(user_id=current_user.user_id).filter(Booking.status != "booked").all()
    #returns empty list if no matching result found |||.first(), .scalar(), .one_or_none() returns None in empty query
    return render_template("user/my_history.html", history=history)


# @user_bp.route("/search_treks", methods=["GET", "POST"])
# @login_required
# def search_treks():
#     if not is_user:
#         flash("Unauthorized Access", "danger")
#         return redirect("/")
#     if request.method == "POST":
#         trek_name = request.form["trek_name"]
#         difficulty = request.form["difficulty"]
#         if not( trek_name and difficulty):
#             treks = Trek.query.filter_by().all()
#             return render_template("user/search_treks.html", treks=treks)
#         treks = Trek.query.filter_by(trek_name=trek_name, difficulty=difficulty).all()
#         return render_template("user/search_treks.html", treks=treks)
#     return render_template("user/search_treks.html")