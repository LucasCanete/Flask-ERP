from flask import Blueprint, render_template, redirect, url_for, flash
from erp_system.utils.wifi import list_networks, connect_to_network
from erp_system.forms import ConnectToWiFiForm


connection_bp = Blueprint("connection_bp", __name__)


#show connection page only if not connected to any network
@connection_bp.route("/connection", methods = ['GET', 'POST'])
def connection_page():
    found_networks = list_networks()
    form = ConnectToWiFiForm()

    if form.validate_on_submit():
        connected = connect_to_network(ssid=form.ssid.data, password=form.password.data)
        if connected:
            flash(f'Conectado a la red {form.ssid.data}!', 'success')
            return redirect(url_for("login_bp.login_page"))

        else:
            flash('No pudo conectarse a la red. Revisa el SSID y Contraseña', 'danger')
            return redirect(url_for("connection_bp.connection_page"))


    return render_template("connection.html", form=form, networks = found_networks)
