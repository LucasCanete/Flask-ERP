from erp_system import app

"""aaaaaaaaa"""
from erp_system.utils.reports import send_pdf_daily_job

"""
This file will be executed by cron (linux) to automatically
send the pdf at a given time.
For the flask frontend this file is not relevant
"""

if __name__ == "__main__":
    with app.app_context():
        send_pdf_daily_job()
