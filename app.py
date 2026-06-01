from flask import Flask
import models
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.sqlite3' 
app.config["SECRET_KEY"] = "super-secret-key-even-though-it-is-not-so-secret"
models.db.init_app(app)
with app.app_context():
    models.db.create_all()
