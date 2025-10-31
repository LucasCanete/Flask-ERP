from apscheduler.schedulers.background import BackgroundScheduler
from erp_system.utils.reports import send_pdf_daily_job
from datetime import datetime, timedelta

def start_scheduler():
    """Inicia el programador (ejecuta de lunes a viernes a las 18:00)."""
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        send_pdf_daily_job,
        trigger="cron",
        day_of_week="mon-sat",  # lunes a viernes
        hour=18,
        minute=0,
        id="daily_pdf_job",
        replace_existing=True,
        #next_run_time=datetime.now() + timedelta(seconds=10)  # 🔥 ejecuta en 10 segundos
    )

    scheduler.start()
    print("Scheduler started: Sending PDF from MON to SAT at 18:00!")
