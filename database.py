from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Customer(db.Model):
    discriminator = db.Column('type', db.String(63))
    __mapper_args__ = {'polymorphic_on': discriminator}
    id = db.Column(db.Integer, primary_key=True)
    orders = db.relationship('Order', backref='customer', lazy=True)

    phone = db.Column(db.String(63))
    email = db.Column(db.String(63))


class Person(Customer):
    __mapper_args__ = {'polymorphic_identity': 'person'}
    id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)

    first_name = db.Column(db.String(63))
    last_name = db.Column(db.String(63))
    birthday = db.Column(db.String(63))


class Company(Customer):
    __mapper_args__ = {'polymorphic_identity': 'company'}
    id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)

    ic = db.Column(db.String(63))
    dic = db.Column(db.String(63))


order_item = db.Table(
    'order_item',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    price = db.Column(db.Integer)
    description = db.Column(db.Text)

    @classmethod
    def create_init_items(cls):
        items = [cls(price=100, description='Cheap item'),
                 cls(price=200, description='Cheapish item'),
                 cls(price=500, description='Expensive item'),
                 cls(price=1000, description='Luxury item')]

        for item in items:
            db.session.add(item)
        db.session.commit()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    items = db.relationship('Item', secondary=order_item)

    total_price = db.Column(db.Integer)
