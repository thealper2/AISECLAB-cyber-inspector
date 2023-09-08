from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_text = db.Column(db.String(500), unique=False)
    label = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    queries = db.relationship("Query")