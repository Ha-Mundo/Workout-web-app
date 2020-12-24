from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    workouts = db.relationship('Workout', backref='author', lazy=True)


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    exercise = db.Column(db.Text(50), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Text(50), nullable=False)
    notes = db.Column(db.Text(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)