from flask import Blueprint, request, render_template
from models import db, WasteLog

waste_bp = Blueprint("waste", __name__)

@waste_bp.route("/waste", methods=["GET", "POST"])
def track_waste():
    if request.method == "POST":
        item_name = request.form["item_name"]
        category = request.form["category"]
        new_waste = WasteLog(item_name=item_name, category=category)
        db.session.add(new_waste)
        db.session.commit()
    return render_template("waste.html")

# Register Blueprint in `app.py`
from routes.waste_routes import waste_bp
app.register_blueprint(waste_bp)
