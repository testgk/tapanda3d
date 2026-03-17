"""
Email verification helper for GeoChallenge.

SMTP settings are read from environment variables so that no credentials are
hard-coded in the source tree:

    SMTP_HOST      – SMTP server hostname  (default: smtp.gmail.com)
    SMTP_PORT      – SMTP server port      (default: 587)
    SMTP_USER      – SMTP login username
    SMTP_PASSWORD  – SMTP login password
    FROM_EMAIL     – Sender address        (defaults to SMTP_USER)

If SMTP_USER or SMTP_PASSWORD are not set the send will raise SendError so
the caller can fall back to displaying the token on-screen for local testing.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendError(Exception):
    """Raised when the verification e-mail cannot be delivered."""


def send_verification_email(to_email: str, nickname: str, token: str) -> None:
    """
    Send a verification e-mail containing *token* to *to_email*.

    Raises SendError if the message cannot be delivered (missing credentials,
    network error, SMTP rejection, etc.).
    """
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    from_email = os.environ.get('FROM_EMAIL', smtp_user)

    if not smtp_user or not smtp_password:
        raise SendError(
            'SMTP_USER and SMTP_PASSWORD environment variables are not set.'
        )

    subject = 'GeoChallenge – Verify your email address'
    body = (
        f'Hello {nickname},\n\n'
        f'Thank you for registering in GeoChallenge!\n\n'
        f'Your verification code is:\n\n'
        f'    {token}\n\n'
        f'Enter this code in the verification screen to activate your account.\n\n'
        f'If you did not register for GeoChallenge, please ignore this email.\n\n'
        f'Best regards,\n'
        f'The GeoChallenge Team'
    )

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as exc:
        raise SendError(f'Failed to send verification email: {exc}') from exc
