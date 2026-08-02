"""
Phase 4 contact form email. Sends the submission straight to CONTACT_EMAIL over
SMTP, off the event loop since smtplib is blocking. Returns False on any
failure so the caller can tell the visitor something went wrong instead of
lying about a message that never sent.
"""

import asyncio
import smtplib
from email.message import EmailMessage

from config import settings


def _send(name: str, email: str, phone: str, message: str) -> bool:
    if not (settings.smtp_user and settings.smtp_password):
        return False

    body = EmailMessage()
    body["Subject"] = f"Eye of Aqaba contact form: {name}"
    body["From"] = settings.smtp_user
    body["To"] = settings.contact_email
    body["Reply-To"] = email
    body.set_content(f"Name: {name}\nEmail: {email}\nPhone: {phone or '(not given)'}\n\n{message}")

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(body)
        return True
    except Exception:
        return False


async def send_contact_email(name: str, email: str, phone: str, message: str) -> bool:
    return await asyncio.to_thread(_send, name, email, phone, message)
