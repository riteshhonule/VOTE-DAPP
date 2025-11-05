from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import random
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# Configure Flask with external templates/static
# ==========================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../templates"),
    static_folder=os.path.join(BASE_DIR, "../static")
)
app.secret_key = "votechori_secret"

# =========================
# DATABASE CONFIG (SQLite)
# =========================
DB_PATH = os.path.join(BASE_DIR, "votechori.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aadhaar TEXT,
            email TEXT UNIQUE,
            wallet_address TEXT,
            has_voted INTEGER DEFAULT 0
        )
    """)

    # Create votes_history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS votes_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT,
            party_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

# =========================
# EMAIL OTP CONFIG
# =========================
SENDER_EMAIL = "riteshhonule@gmail.com"
SENDER_PASSWORD = "abrr osvc rjsp xkci"

otp_storage = {}

def send_otp(email):
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
    return aadhaar_number.isdigit() and len(aadhaar_number) == 12

# =========================
# ROUTES
# =========================
@app.route("/")
def index():
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
    return "❌ Invalid Aadhaar number"

@app.route("/otp")
def otp_page():
    return render_template("otp.html")

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    entered_otp = request.form["otp"]

    if entered_otp == session.get("otp"):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT OR IGNORE INTO users (aadhaar, email)
                VALUES (?, ?)
            """, (session["aadhaar"], session["email"]))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"⚠️ Database Error: {e}")
            return "⚠️ Database error. Please try again."

        return redirect(url_for("wallet"))
    return "❌ Invalid OTP"

@app.route("/wallet")
def wallet():
    return render_template("wallet.html")

@app.route("/save_wallet", methods=["POST"])
def save_wallet():
    wallet = request.json.get("wallet")
    email = session.get("email")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET wallet_address=? WHERE email=?", (wallet, email))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "✅ Wallet saved successfully!"})

@app.route("/vote")
def vote():
    return render_template("vote.html")

@app.route("/mark_voted", methods=["POST"])
def mark_voted():
    data = request.get_json()
    wallet = data.get("wallet")
    party_name = data.get("party_name")

    conn = get_db_connection()
    cur = conn.cursor()

    # Mark user as voted
    cur.execute("UPDATE users SET has_voted=1 WHERE wallet_address=?", (wallet,))

    # Record vote history
    cur.execute("""
        INSERT INTO votes_history (wallet_address, party_name)
        VALUES (?, ?)
    """, (wallet, party_name))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"✅ Vote recorded for {party_name}!"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
