from flask import Flask
import models
app = Flask(__name__.split('.')[0]) #Flask app instance 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.sqlite3' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Improve performance by disabling track modifications
app.config["SECRET_KEY"] = "super-secret-key-even-though-it-is-not-so-secret"
models.db.init_app(app)
with app.app_context(): #Flask app requires an application context to perform database operations, when they are performed outside of defined routes.
    models.db.create_all()
