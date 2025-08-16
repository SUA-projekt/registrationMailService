import os
import json
import smtplib
from email.message import EmailMessage

def handler(request):
    try:
        body = request.get_json()
        user_email = body.get("email")
        user_name = body.get("name", "")
        user_surname = body.get("surname", "")

        if not user_email:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing email"})
            }

        msg = EmailMessage()
        msg["Subject"] = "Welcome to Parking Service!"
        msg["From"] = os.environ["MAIL_FROM"]
        msg["To"] = user_email
        msg.set_content(f"Hi {user_name} {user_surname}, thanks for registering at Parking Service!")

        with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as smtp:
            smtp.starttls()
            smtp.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
            smtp.send_message(msg)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Welcome email sent"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
