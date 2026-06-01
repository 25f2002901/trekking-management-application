from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users' #if not specified, it will be 'User'(Class name) by default
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    contact_no = db.Column(db.String(20), nullable=False) # Assuming contact number is stored as a string to accommodate different formats like plus sign, dashes, etc.
    role = db.Column(db.String(50), nullable=False) # e.g., 'admin', 'user', etc.
    about_me = db.Column(db.Text, nullable=True) #optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #One-to-many relationship with bookings
    bookings = db.relationship('Booking', backref='user', lazy=True) #lazy=True means that the related bookings will be loaded only when accessed, not immediately when the user is queried.
    def __repr__(self):
        return f'<User {self.username}>' #This is a string representation of the User object, which can be useful for debugging and logging. It will display the username when the object is printed.
class Trek(db.Model):
    __tablename__ = 'treks'
    trek_id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending') # 'pending', 'completed', 'approved','open','closed'. 
    price = db.Column(db.Float, nullable=False, default=0)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    #One-to-many relationship with bookings
    bookings = db.relationship('Booking', backref='trek', lazy=True)
    def __repr__(self):
        return f'<Trek {self.trek_name}>'
    
class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.trek_id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='booked') # 'booked', 'completed', 'cancelled'
    def __repr__(self):
        return f'<Booking {self.booking_id}>'
    
class StaffProfile(db.Model):
    __tablename__ = 'staff_profiles'
    staff_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='active')  # active, inactive, on_leave
    user = db.relationship('User', foreign_keys=[staff_id], backref='staff_profile')
    assigned_treks = db.relationship('Trek', backref='assigned_staff', lazy=True, foreign_keys='Trek.assigned_staff_id')
    def __repr__(self):
        return f'<StaffProfile {self.staff_id}>'
    
