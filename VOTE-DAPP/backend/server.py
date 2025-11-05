from flask import Flask, request, jsonify
from flask_cors import CORS
import random, smtplib, os
from dotenv import load_dotenv
from db import init_db, save_vote

load_dotenv()
app = Flask(__name__)
CORS(app)

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

otp_store = {}
aadhaar_verified = {}

# Initialize DB
init_db()

# ✅ Aadhaar Verification (mock API)
@app.route("/verify-aadhaar", methods=["POST"])
def verify_aadhaar():
    data = request.get_json()
    aadhaar = data.get("aadhaar")
    if len(aadhaar) == 12 and aadhaar.isdigit():
        aadhaar_verified[aadhaar] = True
        return jsonify({"success": True, "message": "Aadhaar verified successfully!"})
    return jsonify({"success": False, "message": "Invalid Aadhaar number!"})


# ✅ Send OTP
@app.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    email = data.get("email")
    otp = random.randint(100000, 999999)
    otp_store[email] = otp
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            msg = f"Subject: Voting OTP Verification\n\nYour OTP is: {otp}"
            server.sendmail(EMAIL, email, msg)
        return jsonify({"message": "OTP sent to your email"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Verify OTP
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = int(data.get("otp"))
    if otp_store.get(email) == otp:
        del otp_store[email]
        return jsonify({"success": True})
    return jsonify({"success": False})


# ✅ Save Vote Info to DB
@app.route("/save-vote", methods=["POST"])
def store_vote():
    data = request.get_json()
    aadhaar = data.get("aadhaar")
    email = data.get("email")
    wallet = data.get("wallet")
    party = data.get("party")
    tx_hash = data.get("txHash")

    save_vote(aadhaar, email, wallet, party, tx_hash)
    return jsonify({"success": True, "message": "Vote saved successfully!"})


if __name__ == "__main__":
    app.run(port=5000)
