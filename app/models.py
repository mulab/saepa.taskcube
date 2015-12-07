from . import db
from datetime import timedelta


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), default='')
    email = db.Column(db.Unicode(64), default='')
    mobile = db.Column(db.Unicode(64), default='')
    openid = db.Column(db.Unicode(128), default='', unique=True, index=True)
    credits = db.Column(db.Integer, default=0)
    total_time = db.Column(db.Interval, default=timedelta(0))
    total_distance = db.Column(db.Integer, default=0)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: %s, ID: %s, Credits: %s>' % (self.name, self.openid, self.credits)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Unicode(64))
    name = db.Column(db.Unicode(64))
    credit = db.Column(db.Integer)
    need_validation = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Interval)
    speed = db.Column(db.Float)
    distance = db.Column(db.Integer)
    finished = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.openid'))

    def __repr__(self):
        return '<Task: %s, Credits: %s, User: %s, DateTime: %s>' % \
               (self.name, self.credit, self.user_id, self.datetime)
