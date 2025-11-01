from flask import Blueprint, make_response, render_template
from erp_system.utils.reports import generate_pdf_for_date
from erp_system.forms import DownloadForm
from datetime import datetime

download_bp = Blueprint('download_bp',__name__)

@download_bp.route("/downloads", methods=['GET', 'POST'])
def download_page():

    form = DownloadForm()
    if form.validate_on_submit():
        print(f"Date: {form.chosen_date.data}")
        dt = datetime.strptime(form.chosen_date.data, '%Y-%m-%d').date()
        dt_str = dt.strftime("%d-%m-%Y")
        pdf = generate_pdf_for_date(date=dt)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=reporte_{dt_str}.pdf'
        return response

    return render_template("download_report.html",form=form )
