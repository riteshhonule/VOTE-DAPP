import smtplib
import random
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    msg = MIMEText(f"Your OTP for Vote Verification is {otp}")
    msg["Subject"] = "Vote OTP Verification"
    msg["From"] = EMAIL_USER
    msg["To"] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, email, msg.as_string())
        print("✅ OTP sent successfully to", email)
        return otp
    except Exception as e:
        print("❌ Error sending OTP:", e)
        return None
