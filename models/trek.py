from models import db

class Trek(db.Model):
    __tablename__ = 'treks'
    trek_id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending') #'completed', 'open','closed'. 
    price = db.Column(db.Float, nullable=False, default=0)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    #Many-to-one relation with User(Staff) -> Multiple treks can have the same staff(not at the same time)
    assigned_staff = db.relationship('User',backref= "assigned_treks",lazy= True)
    #One-to-many relationship with bookings
    bookings = db.relationship('Booking', backref='trek', lazy=True, foreign_keys='Booking.trek_id') #foreign_keys is used to specify which foreign key to use for the relationship, since there are multiple foreign keys in the Booking model.
    def __repr__(self):
        return f'<Trek {self.trek_name}>'