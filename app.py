from flask import Flask

from database import db, Item
from views import views

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()
    if not Item.query.all():
        Item.create_init_items()

app.register_blueprint(views)

if __name__ == '__main__':
    app.run()
