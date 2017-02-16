 # -*- coding: utf-8 -*-
from hashlib import md5
from app import db
# from werkzeug.security import generate_password_has, check_password_hash
registrations = db.Table('registrations',
db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    password =db.Column(db.String(128))
    role= db.relationship('Role', backref = 'author',lazy = 'dynamic')
    group = db.relationship('Group',secondary=registrations,backref=db.backref('user', lazy='dynamic'),lazy='dynamic')
    
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.password).hexdigest() + '?d=mm&s=' + str(size)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)



class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    position = db.Column(db.String(140))
    name=db.Column(db.String(64), index = True, unique = True)
    tel=db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    groupname = db.Column(db.String)