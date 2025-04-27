import os
import requests
import logging
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, WasteLog
from datetime import datetime, timedelta
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EARTH911_API_KEY = os.getenv("EARTH911_API_KEY")

# Define Blueprint
waste_bp = Blueprint("waste", __name__)

# Dashboard route
@waste_bp.route("/dashboard")
@login_required
def waste_dashboard():
    try:
        logs = (
            WasteLog.query
                .filter_by(user_id=current_user.id)
                .order_by(WasteLog.created_at.desc())
                .all()
        )
        def chart_data(entries):
            counts = {}
            for e in entries:
                counts[e.category] = counts.get(e.category, 0) + 1
            return counts

        all_time = chart_data(logs)
        recent_entries = [l for l in logs if l.created_at > datetime.utcnow() - timedelta(days=30)]
        recent = chart_data(recent_entries)

        return render_template(
            "dashboard.html",
            logs=logs,
            all_time_chart_data=all_time,
            recent_chart_data=recent,
            error=None
        )
    except Exception as e:
        logging.error("Dashboard error: %s", e)
        return render_template(
            "dashboard.html",
            logs=[],
            all_time_chart_data={},
            recent_chart_data={},
            error=str(e)
        )

# Scan page route
@waste_bp.route("/scan-barcode")
@login_required
def scan_barcode():
    return render_template("barcode_scan.html")

# Cached OpenFoodFacts lookup
@lru_cache(maxsize=500)
def cached_off_lookup(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    res = requests.get(url, timeout=5)
    res.raise_for_status()
    return res.json()

# Earth911 material search by name/category
def search_materials(query):
    try:
        url = "https://api.earth911.com/earth911.searchMaterials"
        params = {"api_key": EARTH911_API_KEY, "query": query}
        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        return res.json().get("result", [])
    except Exception as e:
        logging.error("Material search failed: %s", e)
        return []

# Lookup and classify barcode
@waste_bp.route("/api/lookup-barcode", methods=["POST"])
@login_required
def lookup_barcode():
    data = request.get_json() or {}
    barcode = (data.get("barcode") or "").strip()

    if not barcode:
        return jsonify({"error": "Missing barcode"}), 400

    try:
        off = cached_off_lookup(barcode)
        prod = off.get("product", {})
        name = prod.get("product_name") or prod.get("generic_name") or f"Item {barcode}"
        tags = prod.get("packaging_tags") or []
    except Exception as e:
        logging.error("OFF lookup failed: %s", e)
        name, tags = f"Item {barcode}", []

    materials = search_materials(name)
    if materials:
        category = materials[0].get("material_name", "Other")
    else:
        low = [t.lower() for t in tags]
        if any("plastic" in t for t in low):
            category = "Plastic"
        elif any("metal" in t for t in low):
            category = "Metal"
        elif any("glass" in t for t in low):
            category = "Glass"
        elif any("paper" in t for t in low):
            category = "Paper"
        else:
            category = "Other"

    # ✅ Disposal method logic
    if category in ["Plastic", "Metal", "Glass", "Paper"]:
        disposal_method = "Recycle"
    elif category == "Other":
        disposal_method = "Landfill"
    else:
        disposal_method = "Landfill"

    tips = {
        "Plastic": "Clean and rinse before recycling.",
        "Metal":   "Rinse and recycle with metals.",
        "Glass":   "Rinse and recycle with glass.",
        "Paper":   "Recycle with paper products.",
        "Other":   "Check local recycling guidelines."
    }
    tip = tips.get(category, "Check local recycling guidelines.")

    return jsonify({
        "item_name": name,
        "category": category,
        "tip": tip,
        "disposal_method": disposal_method  # ✅ now included!
    })

# Log waste
@waste_bp.route("/api/log-waste", methods=["POST"])
@login_required
def log_scanned_waste():
    data = request.get_json() or {}
    try:
        entry = WasteLog(
            user_id=current_user.id,
            item_name=data.get("item_name"),
            category=data.get("category")
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        logging.error("Log error: %s", e)
        return jsonify({"error": str(e)}), 500

# Delete a waste log
@waste_bp.route("/api/log-waste/<int:log_id>", methods=["DELETE"])
@login_required
def delete_waste_log(log_id):
    log = WasteLog.query.get_or_404(log_id)

    if log.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(log)
    db.session.commit()
    return jsonify({"success": True})
