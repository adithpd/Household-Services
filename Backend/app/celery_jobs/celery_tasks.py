from app.models.booking.booking_info import BookingInfo
from app.models.customer.customer_info import CustomerInfo
from app.models.user.user_info import UserInfo
from datetime import datetime, timedelta
from app.celery_jobs.emailSender.send_email import send_reminder_email, send_monthly_report_email
from celery.schedules import crontab
from app import create_app, redis_client
import pandas as pd
import os


app, celery = create_app()

@celery.task
def flush_redis_cache():
    redis_client.flushdb()
    
@celery.task
def schedule_reminders():
    with app.app_context():
        today = datetime.today().date()

        upcoming_bookings = BookingInfo.query.filter(
            BookingInfo.start_time >= today, 
            BookingInfo.start_time <= today + timedelta(days=4)
        ).all()

        for booking in upcoming_bookings:
            customer = CustomerInfo.query.filter_by(customer_id=booking.customer_id).first()
            if not customer:
                print(f"No customer found for booking {booking.id}")
                continue

            user = UserInfo.query.filter_by(user_id=customer.user_id).first()
            if not user:
                print(f"No user found for customer {customer.customer_id}")
                continue

            customer_email = user.email
            booking_date = booking.start_time

            for days_before in [1, 2, 3, 4]:
                reminder_date = booking_date - timedelta(days=days_before)
                reminder_time = datetime.combine(reminder_date, datetime.min.time())

                if reminder_date >= today:
                    send_reminder_email.apply_async(
                        args=[customer_email, booking_date],
                        eta=reminder_time
                    )
                    print(f"Reminder scheduled for {customer_email} on {reminder_date}")


@celery.task
def send_monthly_report():
    with app.app_context():
        today = datetime.today().date()
        first_day_of_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_of_last_month = today.replace(day=1) - timedelta(days=1)

        customers = CustomerInfo.query.all()

        for customer in customers:
            user = UserInfo.query.filter_by(user_id=customer.user_id).first()
            if not user:
                print(f"No user found for customer {customer.customer_id}")
                continue

            customer_email = user.email
            customer_name = user.name

            bookings = BookingInfo.query.filter(
                BookingInfo.customer_id == customer.customer_id,
                BookingInfo.start_time >= first_day_of_last_month,
                BookingInfo.start_time <= last_day_of_last_month
            ).all()

            if not bookings:
                continue

            send_monthly_report_email.apply_async(
                args=[customer_email, customer_name, bookings]
            )
            print(f"Monthly report (PDF) sent to {customer_email}")


celery.conf.beat_schedule = {
    "schedule_daily_reminders": {
        "task": "tasks.schedule_reminders",
        "schedule": crontab(hour=0, minute=0),
    },
    "schedule_monthly_reports": {
        "task": "tasks.send_monthly_report",
        "schedule": crontab(day_of_month=1, hour=2, minute=0),
    },
    'flush-redis-every-10-seconds': {
        'task': 'tasks.flush_redis_cache',
        'schedule': 10.0
    }
}

@celery.task
def export_service_requests(service_professional_id):
    with app.app_context():
        print("Entered")
        service_requests = BookingInfo.query.filter_by(service_professional_id=service_professional_id).all()

        if not service_requests:
            return {"status": "failed", "message": "No service requests found."}

        data = []
        for request in service_requests:
            customer = CustomerInfo.query.filter_by(customer_id=request.customer_id).first()
            user = UserInfo.query.filter_by(user_id=customer.user_id).first() if customer else None
            data.append({
                "Booking ID": request.booking_id,
                "Customer Name": user.name if user else "Unknown",
                "Customer Email": user.email if user else "Unknown",
                "Start Time": request.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "End Time": request.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Status": request.status
            })

        df = pd.DataFrame(data)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"service_requests_{service_professional_id}_{timestamp}.csv"
        report_folder = os.path.abspath(os.path.join(os.getcwd(), "report_generated"))
        os.makedirs(report_folder, exist_ok=True)
        file_path = os.path.join(report_folder, filename)

        df.to_csv(file_path, index=False)

        file_url = f"http://127.0.0.1:5000/reports/{filename}"
        return {"status": "success", "file_url": file_url}