from flask import Flask, render_template
from config import Config
from models import db, login_manager
from models.user import User
from models.trek import Trek
from werkzeug.security import generate_password_hash
from routes.auth import bp
from routes.admin import admin_bp
from routes.staff import staff_bp
# from routes.user import user_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.signin" # Redirects to signin page if user tries to access protected routes without authentication.
login_manager.login_message = "Please sign in to access this page." # Message displayed when redirecting to login page.
login_manager.login_message_category = "info" # Category for flash messages when redirecting to login page.

app.register_blueprint(bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
# app.register_blueprint(user_bp)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))


with app.app_context():#Flask app requires an application context to perform database operations, when they are performed outside of defined routes.
    db.create_all()
    admin = User.query.filter_by(email="admin123@gmail.com").first()
    if not admin:
        admin = User(username="Admin",email="admin123@gmail.com", full_name= "Administrator",
            password=generate_password_hash("admin123"), role= "admin", approved= True)
        db.session.add(admin)
        db.session.commit()


@app.route("/")
def home():
    treks = Trek.query.filter_by(
        status="open"
    ).limit(5).all()

    return render_template(
        "home.html",
        treks=treks
    )


if __name__ == "__main__":
    app.run(debug=True)

