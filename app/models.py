from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), default='')
    email = db.Column(db.Unicode(64), default='')
    mobile = db.Column(db.Unicode(64), default='')
    openid = db.Column(db.Unicode(128), default='', unique=True, index=True)
    credits = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User: %s, ID: %s, Credits: %d>' % (self.name, self.openid, self.credits)
