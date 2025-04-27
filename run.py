from app import app       # <-- import your Flask() instance

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    # DEBUG will be False on Heroku because FLASK_ENV=production
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
