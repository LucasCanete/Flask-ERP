import logging

from flask import Blueprint, flash, redirect, render_template, url_for

from erp_system.forms import ConnectToWiFiForm
from erp_system.utils.wifi import connect_to_network, list_networks

logging.basicConfig(level=logging.DEBUG)
connection_bp = Blueprint("connection_bp", __name__)


# show connection page only if not connected to any network
@connection_bp.route("/connection", methods=["GET", "POST"])
def connection_page():
    logging.info("🪧 Entered in Connection")
    found_networks = list_networks()
    form = ConnectToWiFiForm()

    if form.validate_on_submit():
        connected = connect_to_network(ssid=form.ssid.data, password=form.password.data)
        if connected:
            flash(f"Conectado a la red {form.ssid.data}!", "success")
            return redirect(url_for("login_bp.login_page"))

        else:
            flash("No pudo conectarse a la red. Revisa el SSID y Contraseña", "danger")
            return redirect(url_for("connection_bp.connection_page"))

    return render_template("connection.html", form=form, networks=found_networks)
