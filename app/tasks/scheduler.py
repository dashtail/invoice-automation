from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks.invoice import create_invoices

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(create_invoices, 'interval', hours=1)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()
