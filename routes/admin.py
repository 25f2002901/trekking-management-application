from flask import (render_template, request, redirect, url_for, Blueprint, flash)
from flask_login import (login_user, logout_user, login_required, current_user)
from models import db
from models.user import User
from models.trek import Trek
from models.booking import Booking
from datetime import datetime

admin_bp = Blueprint("admin",__name__,url_prefix= "/admin")

def is_admin():
    return (current_user.is_authenticated and current_user.role == "admin")

@admin_bp.route("/admin_dashboard")
@login_required
def admin_dashboard():
    if is_admin():
        total_treks = db.session.query(Trek).count()
        total_users = db.session.query(User).filter_by(role = "user").count()
        total_trek_staff = User.query.filter_by(role = "staff").count() #Same Same but Different!
        #One query is using recommended query format and other is using old format. Both are working fine.
        total_bookings = Booking.query.count()
        return render_template("admin/dashboard.html", total_treks = total_treks, total_users = total_users, total_trek_staff = total_trek_staff, total_bookings = total_bookings)
    return redirect(url_for("auth.signin"))

@admin_bp.route("/manage_treks")
@login_required
def manage_treks():
    if not is_admin():
        return redirect(url_for("auth.signin"))
    treks = Trek.query.all()
    return render_template("admin/manage_treks.html", treks = treks)

@admin_bp.route("/create_trek", methods= ["GET","POST"])
@login_required
def create_trek():
    if not is_admin():
        return redirect(url_for("auth.signin"))
    if request.method == "POST":
        trek = Trek(trek_name = request.form.get("trek_name"),
        location = request.form.get("location"),
        difficulty = request.form.get("difficulty"),
        duration = int(request.form.get("duration")),
        available_slots = int(request.form.get("available_slots")),
        assigned_staff_id = request.form.get("assigned_staff_id"),
        status = request.form.get("status"),
        price = float(request.form.get("price")),
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date(),
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date(),
        notes = request.form.get("notes"))
        db.session.add(trek)
        db.session.commit()
        flash("Trek created successfully!", "success")
        return redirect(url_for("admin.manage_treks"))
    return render_template("admin/create_trek.html")

@admin_bp.route("/update_trek/<int:trek_id>", methods= ["GET","POST"])
@login_required
def update_trek(trek_id):
    if not is_admin():
        return redirect(url_for("auth.signin"))
    trek = Trek.query.get_or_404(trek_id)
    if request.method == "POST":
        trek.trek_name = request.form.get("trek_name")
        trek.location = request.form.get("location")
        trek.difficulty = request.form.get("difficulty")
        trek.duration = int(request.form.get("duration"))
        trek.available_slots = int(request.form.get("available_slots"))
        trek.status = request.form.get("status")
        trek.price = float(request.form.get("price"))
        trek.start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date()
        trek.end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date()
        trek.notes = request.form.get("notes")
        db.session.commit()
        flash("Trek updated successfully!", "success")
        return redirect(url_for("admin.manage_treks"))
    return render_template("admin/update_trek.html", trek=trek)

@admin_bp.route("/delete_trek/<int:trek_id>", methods= ["POST"])
@login_required
def delete_trek(trek_id):
    if not is_admin():
        return redirect(url_for("auth.signin"))
    trek = Trek.query.get_or_404(trek_id)
    Booking.query.filter_by(trek_id= trek_id).update({"trek_id": None, "status": "cancelled"})
    db.session.delete(trek)
    db.session.commit()
    flash("Trek Deleted!", "danger")
    return redirect(url_for("admin.manage_treks"))

@admin_bp.route("/manage_users")
@login_required
def manage_users():
    if not is_admin():
        return redirect(url_for("auth.signin"))
    users = User.query.filter_by(role= "user").all()
    return render_template("admin/manage_users.html", users= users)

@admin_bp.route("/blacklist_user/<int:user_id>", methods= ["POST"])
@login_required
def blacklist_user(user_id):
    if not is_admin():
        return redirect(url_for("auth.signin"))
    user = db.session.query(User).get_or_404(user_id)
    user.blacklisted = True
    if user.role== "staff":
        db.session.query(Trek).filter_by(assigned_staff_id = user.user_id).update({"assigned_staff_id": None})
    db.session.commit()
    flash("User blacklisted successfully!", "warning")
    return redirect(url_for("admin.manage_users"))

@admin_bp.route("/manage_staff")
@login_required
def manage_staff():
    if not is_admin():
        return redirect(url_for("auth.signin"))
    staffs = User.query.filter_by(role= "staff").all()
    return render_template("admin/manage_staff.html", staffs= staffs)

@admin_bp.route('/approve_staff/<int:user_id>')
@login_required
def approve_staff(user_id):
    if not is_admin():
        return redirect(url_for("auth.signin"))
    user = db.session.query(User).get_or_404(user_id)
    user.approved = True
    db.session.commit()
    flash("Staff member approved successfully!", "success")
    return redirect(url_for("admin.manage_staff"))

@admin_bp.route("/assign_staff/<int:trek_id>", methods= ["GET","POST"])
@login_required
def assign_staff(trek_id):
    if not is_admin():
        return redirect(url_for("auth.signin"))
    trek = Trek.query.get_or_404(trek_id)
    staff = User.query.filter_by(role= "staff", approved= True).all()
    if request.method == "POST":
        trek.assigned_staff_id = int(request.form.get("staff_id"))
        db.session.commit()
        flash("Staff assigned successfully!", "success")
        return redirect(url_for("admin.manage_treks"))
    return render_template("admin/assign_staff.html", trek= trek, staffs= staff)

@admin_bp.route("/show_bookings")
@login_required
def show_bookings():
    if not is_admin():
        return redirect(url_for("auth.signin"))
    bookings = Booking.query.all()
    return render_template("admin/show_bookings.html", bookings= bookings)

@admin_bp.route("/search_database", methods= ["GET"])
@login_required
def search_database():
    if not is_admin():
        return redirect(url_for("auth.signin"))
    query_param = request.args.get("query_param", "").strip()
    table = request.args.get("table")
    results = {}
    if query_param:
        is_ID = query_param.isdigit()
        search_ID = int(query_param) if is_ID else None
        if is_ID and table=='user':
            found_user = db.session.query(User).filter_by(user_id= search_ID).all()
            results["users"] = found_user
        elif table=="user":
            found_user = db.session.query(User).filter(User.username.ilike(f"%{query_param}%")).all()
            #Using ilike for case-insensitive search and allowing search by both username and user_id. 
        #filter_by() is suitable for simple equality comparisons. Since this search requires OR conditions and partial matching, filter() with ilike() is used instead.
            results["users"] = found_user

        elif is_ID and table=="trek":
            found_trek = db.session.query(Trek).filter_by(trek_id=search_ID).all()
            results["treks"] = found_trek
        elif table=="trek":
            found_trek = db.session.query(Trek).filter(Trek.trek_name.ilike(f"%{query_param}%")).all()
            results["treks"] = found_trek

        elif is_ID and table=='staff':
            found_staff = db.session.query(User).filter(User.role== 'staff').filter(User.user_id == search_ID).all()
            results["staff"] = found_staff
        elif table=='staff':
            found_staff = db.session.query(User).filter(User.role== 'staff').filter(User.username.ilike(f"%{query_param}%")).all()
            results["staff"] = found_staff
        
        return render_template("admin/search_results.html", results= results, query_param= query_param, table= table)
    flash("Please enter an ID or a name!", "warning")
    return render_template("admin/search_results.html")
    #request.referrer contains the url of the page from which the current request originated. Caution: may return None if user typed URL manually.
    #Therefore, always provide a default fallback value when utilizing it in redirects
    #request.referrer reads the HTTP Referer(Yep, that's how it is spelled!) header sent by the client's browser.