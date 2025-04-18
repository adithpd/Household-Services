import os
import resend
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

resend.api_key = "re_YAPEGCZ5_FVKcUtVMqTjYiaDUzWzPvc5m"

def send_reminder_email(customer_email, booking_date):
    params = {
        "from": "Bookings <onboarding@resend.dev>",
        "to": [customer_email],
        "subject": "Upcoming Booking Reminder",
        "html": f"<strong>Your booking is on {booking_date}. Get ready!</strong>",
    }
    
    print(params)
    email_response = resend.Emails.send(params)
    return email_response

def send_monthly_report_email(customer_email, customer_name, bookings):
    pdf_path = generate_monthly_report_pdf(customer_name, bookings)

    params = {
        "from": "Reports <onboarding@resend.dev>",
        "to": [customer_email],
        "subject": "Your Monthly Booking Report",
        "html": "<p>Attached is your monthly booking report.</p>",
        "attachments": [
            {
                "filename": "Monthly_Report.pdf",
                "content": open(pdf_path, "rb").read(),
                "content_type": "application/pdf"
            }
        ]
    }
    
    print(f"Sending monthly report (PDF) to {customer_email}")
    email_response = resend.Emails.send(params)
    os.remove(pdf_path)
    return email_response

def generate_monthly_report_pdf(customer_name, bookings):
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_pdf.name

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Monthly Booking Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Customer: {customer_name}")

    c.drawString(50, 700, "Your Bookings:")
    y = 680
    for booking in bookings:
        booking_info = f"- {booking.start_time.strftime('%Y-%m-%d')} | Service: {booking.service_name}"
        c.drawString(50, y, booking_info)
        y -= 20

    c.save()
    return pdf_path