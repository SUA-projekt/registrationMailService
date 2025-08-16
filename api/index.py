import os
from fastapi import Request
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import smtplib

async def handler(request: Request):
    data = await request.json()
    user_email = data.get("email")
    user_name = data.get("name", "")
    user_surname = data.get("surname", "")

    if not user_email:
        return JSONResponse(status_code=400, content={"error": "Missing email"})

    msg = EmailMessage()
    msg["Subject"] = "Welcome to Parking Service!"
    msg["From"] = os.getenv("MAIL_FROM")
    msg["To"] = user_email
    msg.set_content(f"Hi {user_name} {user_surname}, thanks for registering at Parking Service!")

    try:
        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            smtp.send_message(msg)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to send email: {str(e)}"})

    return JSONResponse({"message": "Welcome email sent"})

# Vercel handler must be named "app"
from fastapi import FastAPI
app = FastAPI()
app.add_api_route("/", handler, methods=["POST"])
