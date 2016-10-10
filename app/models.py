from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), default='')
    email = db.Column(db.Unicode(64), default='')
    mobile = db.Column(db.Unicode(64), default='')
    openid = db.Column(db.Unicode(128), default='', unique=True, index=True)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: %s, ID: %s>' % (self.name, self.openid)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Unicode(64))
    distance = db.Column(db.Float)
    finished = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.openid'))
    finish_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Task: %s, Credits: %s, User: %s, DateTime: %s>' % \
               (self.key, self.distance, self.user_id, self.finish_time)
