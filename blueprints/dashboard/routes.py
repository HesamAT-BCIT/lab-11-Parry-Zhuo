from __future__ import annotations

import logging
from flask import redirect, render_template, request, session, url_for

from utils.auth import get_current_user
from utils.profile import get_profile_data

from blueprints.api import api_bp
from . import dashboard_bp

# Configure logging (only once per app ideally)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------- API ROUTE ----------------
@api_bp.route("/api/data", methods=["POST"])
def handle_data():
    logger.info("Received data request")

    data = request.get_json()
    logger.info(f"Payload: {data}")

    # Example processing (you can expand this)
    if not data:
        logger.warning("No data received")
        return {"status": "error", "message": "No data provided"}, 400

    logger.info("Data processed successfully")
    return {"status": "success"}, 200


# ---------------- DASHBOARD ROUTE ----------------
@dashboard_bp.route("/")
def home():
    """Home page. Redirects to login if no active session."""
    current_user = get_current_user()

    if current_user:
        profile_data = get_profile_data(current_user)

        return render_template(
            "dashboard.html",
            first_name=profile_data.get("first_name", ""),
            jwt_token=session.get("jwt_token"),
        )

    logger.info("User not authenticated, redirecting to login")
    return redirect(url_for("auth.login"))