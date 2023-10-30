from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks.invoice import create_invoices, get_undelivered_events

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(create_invoices, "interval", hours=3)
    scheduler.add_job(get_undelivered_events, "interval", hours=24)
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
