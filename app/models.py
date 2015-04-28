from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(64))
    mobile = db.Column(db.Unicode(64))
    openid = db.Column(db.Unicode(128), unique=True, index=True)
    credits = db.Column(db.Integer)

    def __repr__(self):
        return '<User: %s, ID: %s>' % (self.name, self.openid)
