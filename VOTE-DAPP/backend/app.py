

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import random
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================
load_dotenv()

# ✅ Define template & static paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# ✅ Initialize Flask app
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "votechori_secret"

# ✅ SQLite Configuration
DB_PATH = os.path.join(BASE_DIR, "votechori.db")


def init_db():
    """Initialize SQLite database if not exists"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aadhaar TEXT,
            email TEXT UNIQUE,
            wallet_address TEXT,
            has_voted INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# =========================
# GMAIL OTP CONFIGURATION
# =========================
SENDER_EMAIL = os.getenv("EMAIL_USER", "riteshhonule@gmail.com")
SENDER_PASSWORD = os.getenv("EMAIL_PASS", "abrr osvc rjsp xkci")  # Use Gmail App Password

otp_storage = {}


def send_otp(email):
    """Generate and send OTP via Gmail SMTP"""
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    subject = "Your OTP Verification Code"
    body = f"Your OTP code is: {otp}\nIt is valid for 5 minutes."

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        server.quit()
        print(f"✅ OTP sent to {email}")
    except Exception as e:
        print(f"❌ Error sending OTP: {e}")

    return otp


def verify_aadhaar(aadhaar_number):
    """Simple Aadhaar number validation"""
    return aadhaar_number.isdigit() and len(aadhaar_number) == 12


# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    """Home page for Aadhaar verification"""
    return render_template("index.html")


@app.route("/verify_aadhaar", methods=["POST"])
def verify_aadhaar_route():
    aadhaar = request.form["aadhaar"]
    email = request.form["email"]

    if verify_aadhaar(aadhaar):
        otp = send_otp(email)
        session["otp"] = otp
        session["aadhaar"] = aadhaar
        session["email"] = email
        return redirect(url_for("otp_page"))

    # ❌ Invalid Aadhaar — show styled error page
    return render_template("error.html")


@app.route("/otp")
def otp_page():
    """Step 2: OTP input page"""
    return render_template("otp.html")


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    """Step 3: Verify OTP and save user"""
    entered_otp = request.form["otp"]

    if entered_otp == session.get("otp"):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT OR IGNORE INTO users (aadhaar, email) VALUES (?, ?)",
                (session["aadhaar"], session["email"]),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Database Error: {e}")
            return "⚠️ Database error. Please try again."

        return redirect(url_for("wallet"))

    return render_template("error.html", message="❌ Invalid OTP. Please try again.")


@app.route("/wallet")
def wallet():
    """Step 4: Wallet connection page"""
    return render_template("wallet.html")


@app.route("/save_wallet", methods=["POST"])
def save_wallet():
    """Save wallet address to user record"""
    wallet = request.json.get("wallet")
    email = session.get("email")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET wallet_address=? WHERE email=?", (wallet, email))
    conn.commit()
    conn.close()
    return jsonify({"message": "✅ Wallet saved successfully!"})


@app.route("/vote")
def vote():
    """Step 5: Voting page"""
    return render_template("vote.html")


@app.route("/mark_voted", methods=["POST"])
def mark_voted():
    """Mark user as voted"""
    wallet = request.json.get("wallet")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET has_voted=1 WHERE wallet_address=?", (wallet,))
    conn.commit()
    conn.close()
    return jsonify({"message": "✅ Vote marked in database!"})


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
