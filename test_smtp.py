
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def test_smtp_connection():
    email = os.getenv('DJANGO_EMAIL_HOST_USER')
    password = os.getenv('DJANGO_EMAIL_HOST_PASSWORD')
    host = os.getenv('DJANGO_EMAIL_HOST', 'smtp.gmail.com')
    port = 587
    
    print(f"Testing SMTP connection to {host}:{port}")
    print(f"User: {email}")
    # print(f"Password starts with: {password[:2]}...") 
    
    try:
        msg = EmailMessage()
        msg.set_content("This is a test email from the debug script.")
        msg['Subject'] = "SMTP Config Test"
        msg['From'] = email
        msg['To'] = email # Send to self
        
        server = smtplib.SMTP(host, port)
        server.set_debuglevel(1)
        server.starttls()
        server.login(email, password)
        server.send_message(msg)
        server.quit()
        print("✅ SMTP Email sent successfully!")
    except Exception as e:
        print(f"❌ SMTP Failed: {e}")

if __name__ == "__main__":
    test_smtp_connection()
