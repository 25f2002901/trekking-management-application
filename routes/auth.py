from flask import (render_template, request, redirect, url_for, Blueprint, flash)
from flask_login import (login_user, logout_user, login_required)
from werkzeug.security import (generate_password_hash,check_password_hash)
from models import db
from models.user import User

bp = Blueprint("auth",__name__,url_prefix= "/auth")


@bp.route("/signin", methods= ['GET','POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.session.query(User).filter_by(email = email).first()
        if not user:
            flash("Invalid Credentials! Unable to Login.",'danger')
            return redirect(url_for('auth.signin'))
        if not check_password_hash(user.password, password):
            flash("Invalid Credentials! Unable to Login.",'danger')
            return redirect(url_for('auth.signin'))
        if user.blacklisted == True:
            flash("Account Blacklisted! Please contact support for more information.",'danger')
            return redirect(url_for('auth.signin'))
        if user.role == "staff" and user.approved == False:
            flash("Pending for approval",'warning')
            return redirect(url_for('auth.signin'))
        login_user(user)
        flash("You have been logged in successfully!",'success')

        #RBAC
        if user.role == "admin":
            return redirect(url_for('admin.admin_dashboard'))
        elif user.role == "staff":
            return redirect(url_for('staff.staff_dashboard'))
        else:
            return redirect(url_for('user.user_dashboard'))
    return render_template('auth/signin.html')

@bp.route("/signup",methods= ['GET',"POST"])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        contact_no = request.form.get('contact_no')
        role = request.form.get("role")

        if role == "admin":
            flash('Invalid Request! Admin cannot be registered.', 'danger')
            return redirect(url_for("auth.signup"))

        already_present = db.session.query(User).filter_by(email = email).first()
        if already_present:
            flash('User with same credentials already present. Please Sign in or Register with different credentials.','danger')
            return redirect(url_for('auth.signup'))
        
        user = User(username= username, email= email, password= generate_password_hash(password),
                    full_name= full_name, contact_no= contact_no, role= role)
        
        if role == 'user':
            user.approved = True
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful! Please Login.",'success')
        return redirect(url_for('auth.signin'))
    
    return render_template('auth/signup.html')

@bp.route("/logout")
@login_required
def logout():
    logout_user() #Clears the user session data 
    flash("You have been logged out successfully!",'success')
    return redirect(url_for('auth.signin'))