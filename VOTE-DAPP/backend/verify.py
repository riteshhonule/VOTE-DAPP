import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURE YOUR EMAIL HERE ---
SENDER_EMAIL = "riteshhonule@gmail.com"
SENDER_PASSWORD = "abrr osvc rjsp xkci"
# Store OTPs temporarily
otp_storage = {}

def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp
    send_otp_email(email, otp)
    return otp

def send_otp_email(to_email, otp):
    subject = "Your OTP Verification Code"
    body = f"Your OTP code is: {otp}\nIt is valid for 5 minutes."

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"✅ OTP sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Error sending OTP: {e}")

def verify_otp(email, entered_otp):
    saved_otp = otp_storage.get(email)
    if saved_otp and saved_otp == entered_otp:
        return True
    return False
