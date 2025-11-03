from flask import Blueprint, render_template, flash, redirect, url_for, request
from erp_system import db
from erp_system.models import Sale
from erp_system.forms import SaleForm
from flask_login import login_required
from datetime import datetime, timedelta
from collections import defaultdict


sale_bp = Blueprint("sale_bp",__name__)


@sale_bp.route("/sales_view", methods = ['GET', 'POST'])
@login_required
def sale_page():
    customer_filter = request.args.get("customer")
    payment_method_filter = request.args.get("payment_method")
    date_filter = request.args.get("date") #str type
    sales = Sale.query

    if customer_filter:
        sales = sales.filter_by(customer=customer_filter)

    if payment_method_filter:
        sales = sales.filter_by(payment_method=payment_method_filter)

    if date_filter:
        selected_date = datetime.strptime(date_filter, "%Y-%m-%d") # convert to datetime obj
        start_datetime = selected_date
        end_datetime = selected_date + timedelta(days=1)  # exclusivo
        sales = sales.filter(Sale.datetime >= start_datetime,
                                Sale.datetime < end_datetime)

    sales = sales.order_by(Sale.datetime.desc()).all()

    grouped = defaultdict(list)

    for sale in sales:
        day_str = sale.datetime.strftime("%d/%m/%Y")
        grouped[day_str].append(sale)

    # Convertir a lista de tuplas ordenada por fecha (reciente primero)
    grouped_sales = sorted(grouped.items(), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"), reverse=True)

    return render_template("sales.html", sales=sales, grouped_sales=grouped_sales)


@sale_bp.route("/new_sale", methods = ['GET', 'POST'])
@login_required
def create_sale_page():
    form = SaleForm()
    if form.validate_on_submit():
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
            sale = Sale(customer=form.customer.data, product=form.product.data, qty=form.qty.data,
                    price_paid=form.price_paid.data, payment_method=form.payment_method.data)
            db.session.add(sale)
            db.session.commit()
            flash(f"Nueva venta ha sido creada!", "success")
            return redirect(url_for('sale_bp.sale_page'))
    return render_template("create_sale.html", form=form)



@sale_bp.route("/edit_sale/<id>", methods=['GET', 'POST'])
@login_required
def edit_sale_page(id):
    form = SaleForm()

    sale = Sale.query.filter_by(id=id).first()
    if not sale:
        flash("Venta no encontrada.", "danger")
        return redirect(url_for("sale_bp.sale_page"))

    #Prefill the form with the values from the service
    if request.method == 'GET':
        form.customer.data = sale.customer
        form.product.data = sale.product
        form.qty.data = sale.qty
        form.price_paid.data = sale.price_paid
        form.payment_method.data = sale.payment_method

    if form.validate_on_submit():
        sale.customer = form.customer.data
        sale.product = form.product.data
        sale.qty = form.qty.data
        sale.price_paid = form.price_paid.data
        sale.payment_method = form.payment_method.data
        db.session.commit()
        flash(f'Venta ha sido editada!','success')
        return redirect(url_for("sale_bp.sale_page"))

    return render_template("edit_sale.html", title="Editar Venta", form=form, sale=sale )

@sale_bp.route("/delete_sale/<id>", methods=['POST'])
@login_required
def delete_sale(id):
    sale = Sale.query.filter_by(id=id).first()
    if sale:
        db.session.delete(sale)
        db.session.commit()
        flash('Venta eliminada correctamente.', 'success')
    else:
        flash('Venta no encontrada.', 'danger')
    return redirect(url_for("sale_bp.sale_page"))
