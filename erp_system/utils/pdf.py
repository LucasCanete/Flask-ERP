"""
Generate a pdf from an html file
"""
from flask import render_template, current_app
from weasyprint import HTML
from erp_system.models import Service
from erp_system.models import Sale
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

def generate_pdf(pdf_name:str):
    today = datetime.today()
    start_datetime = today.date()
    end_datetime = start_datetime + timedelta(days=1)  # exclusivo


    sales = Sale.query
    sales = sales.filter(Sale.datetime >= start_datetime,
                           Sale.datetime < end_datetime)
    today_sales = sales.order_by(Sale.datetime.desc()).all()

    services = Service.query
    services = services.filter(Service.datetime >= start_datetime,
                           Service.datetime < end_datetime)
    today_services = services.order_by(Service.datetime.desc()).all()


    total_sales_price = sum(s.price_paid for s in today_sales)


    logo_path = os.path.join(current_app.root_path, 'static', 'img', 'logo.png')
    logo_uri = 'file://' + logo_path  # convierte a file URI

    #render
    html_content = render_template('report_template.html',logo_path=logo_uri ,sales=today_sales,
                                services=today_services, fecha_actual=datetime.now().strftime('%d/%m/%Y'),
                                total_sales_price=total_sales_price)
    # html to pdf
    pdf = HTML(string=html_content).write_pdf(pdf_name)
    return pdf


def send_pdf_telegram(token, chat_id, file_path):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(file_path, "rb") as pdf:
        requests.post(url, data={"chat_id": chat_id}, files={"document": pdf})


def send_pdf_job():
    today = datetime.today()
    t = today.strftime('%d-%m-%Y')
    report_name = "reporte_" + t +".pdf"

    generate_pdf(report_name)
    
    pdf_path = '/home/lucas/Documents/portalpy/erp/' + report_name
    id = os.getenv("BOT_CHAT_ID")
    token = os.getenv("BOT_TOKEN")

    send_pdf_telegram(token=token, chat_id=id, file_path=pdf_path)
