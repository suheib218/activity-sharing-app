from . import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    mobilenumber = db.Column(db.String(20), nullable=False)  # Changed to String for country code support
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    
    # Relationship with activities created by user
    activities = db.relationship('Activity', backref='organizer', lazy=True)
    # Relationship with activities the user has joined
    joined_activities = db.relationship('Participation', backref='participant', lazy=True)

 


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    date_time = db.Column(db.DateTime, nullable=False)  # Updated column
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    participants = db.relationship('Participation', backref='activity', lazy=True)


class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'activity_id', name='unique_participation'),)

    