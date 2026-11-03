"""
PennyWise - Personal Expense Tracker
Entry Point: app.py
Python Flask Application with Object-Oriented Backend & SQLite Persistence

Features:
- REST API communicating directly with OOP domain models
- Serves responsive HTML5/CSS3/Vanilla JS frontend
- Robust SQLite database integration
- Strict separation between HTTP delivery and OOP domain logic
"""

import os
from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
from routes.api import api_bp
from database.db_manager import DatabaseManager


def create_app(test_config=None) -> Flask:
    """Application factory for PennyWise Flask backend."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static"
    )

    # Enable Cross-Origin Resource Sharing for modern browser frontend interactions
    CORS(app)

    # Register API blueprint
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        """Serves the main application dashboard."""
        return render_template("index.html")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "error": "The requested resource was not found."
        }), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "success": False,
            "error": "An internal server error occurred."
        }), 500

    return app


# Create global app instance
app = create_app()

if __name__ == "__main__":
    # Ensure database is initialized
    db = DatabaseManager("pennywise.db")
    
    # Use FLASK_PORT or 5000 so it doesn't collide with container router ports
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1")
    print(f"==================================================")
    print(f"  PennyWise - Personal Expense Tracker")
    print(f"  Architecture: Python OOP + Flask + SQLite")
    print(f"  Starting server on http://0.0.0.0:{port}")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=debug)
