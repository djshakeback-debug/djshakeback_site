from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# EMAIL SETTINGS
GMAIL_USER = "djshakeback@gmail.com"
GMAIL_APP_PASSWORD = "FloridaBoyDj352!"


def send_booking_email(name, email, phone, service, event_date, details):
    subject = "New DJ Booking Request"
    body = f"""
New Booking Request

Name: {name}
Email: {email}
Phone: {phone}
Service: {service}
Event Date: {event_date}
Details: {details}
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_USER

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.send_message(msg)
    server.quit()


@app.route("/submit-booking", methods=["POST"])
def submit_booking():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    service = request.form.get("service")
    event_date = request.form.get("event_date")
    details = request.form.get("details")

    with open("bookings.txt", "a") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Phone: {phone}\n")
        file.write(f"Service: {service}\n")
        file.write(f"Event Date: {event_date}\n")
        file.write(f"Details: {details}\n")
        file.write("-" * 40 + "\n")

    send_booking_email(name, email, phone, service, event_date, details)

    return """
    <h1>Booking Received!</h1>
    <p>Thanks for booking DJ Shakeback.</p>
    <a href='/home'>Back Home</a>
    """


@app.route("/admin")
def admin():

    with open("bookings.txt", "r") as file:
        bookings = file.read()

    return f"""
    <h1>DJ Shakeback Booking Requests</h1>
    <pre>{bookings}</pre>
    """


if __name__ == "__main__":
    app.run(debug=True)