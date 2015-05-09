from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), default='')
    email = db.Column(db.Unicode(64), default='')
    mobile = db.Column(db.Unicode(64), default='')
    openid = db.Column(db.Unicode(128), default='', unique=True, index=True)
    credits = db.Column(db.Integer, default=0)
    tasks = db.relationship('Task', backref='user')

    def __repr__(self):
        return '<User: %s, ID: %s, Credits: %d>' % (self.name, self.openid, self.credits)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    credit = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.openid'))

    def __repr__(self):
        return '<Task: %s, Credits: %s, User: %d, DateTime: %s>' % \
               (self.name, self.credits, self.user_id, str(self.datetime))
