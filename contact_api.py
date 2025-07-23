from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr
import aiosmtplib
from email.message import EmailMessage
import asyncio
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://eshkol.vercel.app",
        "https://backend-esh.onrender.com",
        "https://eshkol.in"

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

YOUR_EMAIL = "info@kodaicoolstay.com"
YOUR_EMAIL_PASSWORD = "Aash@1006"  # ⚠️ Consider using environment variables in production

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 587

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/contact")
async def send_contact_email(
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone: str = Form(""),
    message: str = Form(...)
):
    # 1. Send form details to yourself
    msg_to_self = EmailMessage()
    msg_to_self["From"] = YOUR_EMAIL
    msg_to_self["To"] = YOUR_EMAIL
    msg_to_self["Subject"] = "New Contact Form Submission"
    msg_to_self.set_content(
        f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
    )

    await aiosmtplib.send(
        msg_to_self,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=YOUR_EMAIL,
        password=YOUR_EMAIL_PASSWORD,
    )

    # 2. Send auto-reply to the user
    msg_to_user = EmailMessage()
    msg_to_user["From"] = YOUR_EMAIL
    msg_to_user["To"] = email
    msg_to_user["Subject"] = "Thank you for contacting Eshkol"
    msg_to_user.set_content(
        f"Hi {name},\n\nThank you for reaching out to Eshkol. We have received your message and will contact you soon.\n\nBest regards,\nEshkol Team"
    )

    await aiosmtplib.send(
        msg_to_user,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=YOUR_EMAIL,
        password=YOUR_EMAIL_PASSWORD,
    )

    return {"success": True, "message": "Emails sent!"}

@app.post("/book")
async def send_booking_email(
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone: str = Form(...),
    service: str = Form(...),
    message: str = Form("")
):
    # 1. Send booking details to yourself
    msg_to_self = EmailMessage()
    msg_to_self["From"] = YOUR_EMAIL
    msg_to_self["To"] = YOUR_EMAIL
    msg_to_self["Subject"] = "New Booking Submission"
    msg_to_self.set_content(
        f"Name: {name}\nEmail: {email}\nPhone: {phone}\nService: {service}\n\nMessage:\n{message}"
    )

    await aiosmtplib.send(
        msg_to_self,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=YOUR_EMAIL,
        password=YOUR_EMAIL_PASSWORD,
    )

    # 2. Send auto-reply to the user
    msg_to_user = EmailMessage()
    msg_to_user["From"] = YOUR_EMAIL
    msg_to_user["To"] = email
    msg_to_user["Subject"] = "Thank you for your booking at Eshkol"
    msg_to_user.set_content(
        f"Hi {name},\n\nThank you for your booking request for '{service}'. We have received your details and will contact you soon to confirm your reservation.\n\nBest regards,\nEshkol Team"
    )

    await aiosmtplib.send(
        msg_to_user,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=YOUR_EMAIL,
        password=YOUR_EMAIL_PASSWORD,
    )

    return {"success": True, "message": "Booking emails sent!"}

# --- Keep-alive background task ---
async def keep_alive():
    await asyncio.sleep(10)  # Wait a bit for server to start
    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.get("https://backend-esh.onrender.com/health", timeout=10)
        except Exception:
            pass
        await asyncio.sleep(180)  # 3 minutes

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_alive())


