import os
import smtplib
from pathlib import Path
from email.message import EmailMessage

from dotenv import load_dotenv


# ============================================================
# PROJECT / ENVIRONMENT CONFIG
# ============================================================

# alert_engine.py is inside:
# D:\Data Analytics\inventory_project\src\
#
# Therefore:
# parent       = src
# parent.parent = inventory_project

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

# Explicitly load the project's .env file
load_dotenv(dotenv_path=ENV_FILE)


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# ============================================================
# VALIDATE EMAIL CONFIGURATION
# ============================================================

def validate_email_config():

    missing = []

    if not EMAIL_SENDER:
        missing.append("EMAIL_SENDER")

    if not EMAIL_PASSWORD:
        missing.append("EMAIL_PASSWORD")

    if not EMAIL_RECEIVER:
        missing.append("EMAIL_RECEIVER")

    if missing:

        raise ValueError(
            "Missing email configuration in .env: "
            + ", ".join(missing)
            + f"\n\nExpected .env location:\n{ENV_FILE}"
        )


# ============================================================
# CREATE EMAIL CONTENT
# ============================================================

def create_reorder_email(result):

    store_id = result.get("store_id", "N/A")
    product_id = result.get("product_id", "N/A")
    supplier_id = result.get("supplier_id", "N/A")

    current_stock = result.get("current_stock", "N/A")
    forecast_demand = result.get("forecast_demand", "N/A")

    lead_time = result.get("lead_time_days", "N/A")
    reorder_point = result.get("reorder_point", "N/A")
    order_quantity = result.get("order_quantity", "N/A")

    procurement_decision = result.get(
        "procurement_decision",
        "N/A"
    )

    supplier_rating = result.get(
        "supplier_rating",
        "N/A"
    )

    recommendation = result.get(
        "recommendation",
        "N/A"
    )

    subject = (
        f"Inventory Reorder Alert - "
        f"{store_id} / {product_id}"
    )

    body = f"""
INVENTORY REORDER ALERT
=======================

A reorder has been triggered by the inventory management system.

Store ID              : {store_id}
Product ID            : {product_id}

Current Stock         : {current_stock}
Forecast Demand       : {forecast_demand}
Reorder Point         : {reorder_point}

Order Quantity        : {order_quantity}

Supplier ID           : {supplier_id}
Lead Time             : {lead_time} days

Supplier Rating       : {supplier_rating}
Recommendation        : {recommendation}
Procurement Decision  : {procurement_decision}


This alert was generated automatically by the
Inventory Management System.

Please review the purchase order and procurement status.

Regards,
Inventory Management System
"""

    return subject, body


# ============================================================
# SEND REORDER ALERT
# ============================================================

def send_reorder_alert(result):

    # --------------------------------------------------------
    # 1. Validate configuration
    # --------------------------------------------------------

    validate_email_config()

    # --------------------------------------------------------
    # 2. Create email
    # --------------------------------------------------------

    subject, body = create_reorder_email(result)

    msg = EmailMessage()

    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    msg.set_content(body)

    # --------------------------------------------------------
    # 3. Connect to Gmail SMTP
    # --------------------------------------------------------

    print("\nConnecting to Gmail SMTP...")

    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    ) as server:

        server.starttls()

        # Login using Gmail App Password
        server.login(
            EMAIL_SENDER,
            EMAIL_PASSWORD
        )

        # Send email
        server.send_message(msg)

    # --------------------------------------------------------
    # 4. Success message
    # --------------------------------------------------------

    print("\n✓ EMAIL ALERT SENT SUCCESSFULLY")

    print(
        f"  From : {EMAIL_SENDER}"
    )

    print(
        f"  To   : {EMAIL_RECEIVER}"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("                 EMAIL ALERT TEST")
    print("=" * 60)

    print(
        f"\nLoading .env from:\n{ENV_FILE}"
    )

    # --------------------------------------------------------
    # Check whether configuration was loaded
    # --------------------------------------------------------

    print(
        "\nEMAIL_SENDER loaded   :",
        bool(EMAIL_SENDER)
    )

    print(
        "EMAIL_PASSWORD loaded :",
        bool(EMAIL_PASSWORD)
    )

    print(
        "EMAIL_RECEIVER loaded :",
        bool(EMAIL_RECEIVER)
    )

    # --------------------------------------------------------
    # Fake result ONLY for testing email functionality
    # --------------------------------------------------------

    test_result = {

        "store_id": "S001",

        "product_id": "P0008",

        "supplier_id": "SUP_9",

        "current_stock": 135,

        "forecast_demand": 97.33,

        "lead_time_days": 8.19,

        "reorder_point": 1284.97,

        "order_quantity": 1832,

        "supplier_rating": "EXCELLENT",

        "recommendation": "PREFERRED",

        "procurement_decision": "PROCEED"
    }

    print("\nSending test email...")

    send_reorder_alert(test_result)

    print("\n" + "=" * 60)
    print("                    TEST COMPLETE")
    print("=" * 60)