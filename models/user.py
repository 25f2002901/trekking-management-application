from models import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users' #if not specified, it will be 'User'(Class name) by default
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    contact_no = db.Column(db.String(20)) # Assuming contact number is stored as a string to accommodate different formats like plus sign, dashes, etc.
    role = db.Column(db.String(50), nullable=False) # e.g., 'admin', 'user', etc.
    approved = db.Column(db.Boolean, default=False, nullable=False)
    blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #One-to-many relationship with bookings
    bookings = db.relationship('Booking', backref='user', foreign_keys='Booking.user_id', lazy=True)#lazy=True means that the related objects will be loaded only when they are accessed, which can improve performance by avoiding unnecessary database queries.

    def get_id(self):
        return str(self.user_id)
    def __repr__(self):
        return f'<User {self.username}>' 
    #This is a string representation of the User object, which can be useful for debugging and logging. It will display the username when the object is printed.
    

#Backref creates an accessor, that is used to specify the name of the attribute that will be added to the related model (Booking in this case) to allow access to the related User object. 
#In this case, it will add a user attribute to the Booking model, which can be used to access the associated User object for a given Booking.