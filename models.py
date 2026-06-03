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
    role = db.Column(db.String(50), nullable=False, default='user') # e.g., 'admin', 'user', etc.
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #One-to-many relationship with bookings
    bookings = db.relationship('Booking', backref='user', foreign_keys='Booking.user_id', lazy=True)#lazy=True means that the related objects will be loaded only when they are accessed, which can improve performance by avoiding unnecessary database queries.
    def __repr__(self):
        return f'<User {self.username}>' #This is a string representation of the User object, which can be useful for debugging and logging. It will display the username when the object is printed.
    @property 
    def is_active(self): 
        return self.active
class Trek(db.Model):
    __tablename__ = 'treks'
    trek_id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff_profiles.staff_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending') # 'pending', 'completed', 'approved','open','closed'. 
    price = db.Column(db.Float, nullable=False, default=0)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    #One-to-many relationship with bookings
    bookings = db.relationship('Booking', backref='trek', lazy=True, foreign_keys='Booking.trek_id') #foreign_keys is used to specify which foreign key to use for the relationship, since there are multiple foreign keys in the Booking model.
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
    
class Staff_Profile(db.Model):
    __tablename__ = 'staff_profiles'
    staff_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='active') # 'active', 'inactive', 'suspended'
    assigned_treks = db.relationship('Trek', backref='assigned_staff', lazy=True) #One-to-many relationship with treks 
    #Only one foreign key is pointing to users table, so foreign_keys argument is not needed here.
    user = db.relationship('User', backref='staff_profile', uselist=False) #One-to-one relationship with User model 
    #uselist=False indicates that this relationship should be treated as a one-to-one relationship, meaning that each Staff_Profile is associated with exactly one User and vice versa.
    def __repr__(self):
        return f'<Staff_Profile {self.staff_id}>'

#Backref creates an accessor, that is used to specify the name of the attribute that will be added to the related model (User in this case) to allow access to the related Staff_Profile object. 
#In this case, it will add a staff_profile attribute to the User model, which can be used to access the associated Staff_Profile object for a given User.