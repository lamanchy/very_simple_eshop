from flask import render_template, request, url_for, redirect, Blueprint

import database
from database import *

views = Blueprint('', __name__, template_folder='templates')


@views.get('/')
def index():
    title = 'Very simple e-shop'
    customers = Customer.query.all()

    return render_template('index.html', **locals())


@views.get('/add_customer/')
def add_customer():
    title = 'Add customer'
    go_back_url = url_for('index')

    return render_template('add_customer.html', **locals())


@views.get('/add_customer/<string:type_of_customer>/')
def add_specific_customer(type_of_customer):
    other = 'person' if type_of_customer == 'company' else 'company'
    title = f'Add customer ({type_of_customer.capitalize()})'
    go_back_url = url_for('add_customer')

    return render_template('add_specific_customer.html', **locals())


@views.get('/customers/<int:id>/')
def show_customer(id):
    title = 'Customer detail'
    go_back_url = url_for('index')
    customer = Customer.query.get_or_404(id)

    return render_template('customer.html', **locals())


@views.get('/customers/<int:customer_id>/orders/<int:order_id>/')
def show_order(customer_id, order_id):
    title = 'Order detail'
    go_back_url = url_for('show_customer', id=customer_id)
    order = Order.query.get_or_404(order_id)

    return render_template('order.html', **locals())


@views.get('/customers/<int:customer_id>/orders/<int:order_id>/add_items/')
def add_items(customer_id, order_id):
    title = 'Add items to order'
    go_back_url = url_for('show_order', customer_id=customer_id, order_id=order_id)
    items = Item.query.all()
    order = Order.query.get_or_404(order_id)

    return render_template('add_items.html', **locals())


@views.post('/create_customer/')
def create_customer():
    type_of_customer = request.args['type_of_customer']
    model = getattr(database, type_of_customer.capitalize())(**request.form)
    db.session.add(model)
    db.session.commit()
    # if errors would be present then something like:
    #   redirect(url_for('add_specific_customer', type_of_customer, errors='error_to_show', filled_values=request.form))

    return redirect(url_for('show_customer', id=model.id))


@views.post('/new_order/')
def new_order():
    customer_id = request.args['customer_id']
    order = Order(
        total_price=0,
        customer_id=customer_id
    )
    db.session.add(order)
    db.session.commit()

    return redirect(url_for('show_order', customer_id=customer_id, order_id=order.id))


@views.post('/toggl_item/')
def toggl_item():
    order_id, item_id, source = request.args['order_id'], request.args['item_id'], request.args['source']
    order = Order.query.get_or_404(order_id)
    item = Item.query.get_or_404(item_id)

    if item in order.items:
        order.items.remove(item)
    else:
        order.items.append(item)

    order.total_price = sum([item.price for item in order.items])
    db.session.add(order)
    db.session.commit()

    return redirect(url_for(source, customer_id=order.customer_id, order_id=order_id))
