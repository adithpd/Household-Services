# Household-Services-Application

# Kill Tasks in Port numbers
sudo lsof -ti :4243 | xargs sudo kill -9
sudo lsof -ti :6379 | xargs sudo kill -9
sudo lsof -ti :4281 | xargs sudo kill -9


# Run Commands in Order
redis-server
export FLASK_APP=run.py
celery -A run.celery worker --loglevel=info
celery -A run.celery beat --loglevel=info
flask run // python run.py
flask shell

# Inside Flask Shell (For quick testing celery tasks)
flask shell or python
from app.celery_jobs.emailSender.send_email import send_reminder_email, send_monthly_report
send_reminder_email("21f1002580@ds.study.iitm.ac.in", "2025-04-01")

from app.celery_jobs.celery_tasks import export_service_requests
export_service_requests("c351cefc83eb4188b761c61707b7688b")