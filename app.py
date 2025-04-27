import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models import db, User
import openai
from datetime import datetime

# Load environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

# Create Flask app
app = Flask(__name__)

# Config settings
# Normalize DATABASE_URL for SQLAlchemy compatibility
raw_db_url = os.getenv("DATABASE_URL") or ""
if raw_db_url.startswith("postgres://"):
    raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = raw_db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "True").lower() == "true"
app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
app.config["EARTH911_API_KEY"] = os.getenv("EARTH911_API_KEY")

# Validate environment variables
missing = []
if not app.config["SQLALCHEMY_DATABASE_URI"] or "your_database_url" in app.config["SQLALCHEMY_DATABASE_URI"]:
    missing.append("DATABASE_URL")
if not app.config["SECRET_KEY"]:
    missing.append("SECRET_KEY")
if not app.config.get("OPENAI_API_KEY"):
    missing.append("OPENAI_API_KEY")
if not app.config.get("EARTH911_API_KEY"):
    missing.append("EARTH911_API_KEY")
if missing:
    raise ValueError(f"❌ Missing or invalid environment variables: {', '.join(missing)}")

# Initialize OpenAI
openai.api_key = app.config["OPENAI_API_KEY"]

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
from trashtrack.routes.auth_routes import auth_bp
from trashtrack.routes.waste_routes import waste_bp
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(waste_bp, url_prefix="/waste")

# Core routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/privacy-policy")
def privacy_policy():
    effective_date = datetime.now().strftime("%B %d, %Y")
    return render_template("privacy_policy.html", effective_date=effective_date)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

# Inject current year into templates
@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

# Run app
if __name__ == "__main__":
    # Use 127.0.0.1 to enable getUserMedia without HTTPS
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=app.config["DEBUG"])
