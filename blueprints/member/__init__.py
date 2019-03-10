import random, logging
from blueprints import db
from flask_restful import fields

from blueprints.detail_member import *

class Member(db.Model):

    __tablename__ = "member"

    id_member = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nama_depan = db.Column(db.String(255))
    nama_belakang = db.Column(db.String(255))
    username = db.Column(db.String(255), unique = True)
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))
    status = db.Column(db.String(50))
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # tokos = db.relationship('Toko', backref = 'id_member', lazy = True)
    # pembelians = db.relationship('Pembelian', backref = 'id_pembeli', lazy = True)
    # details = db.relationship('DetailMember', backref = 'id_member', lazy = True)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_member' : fields.Integer,
        'nama_depan' : fields.String,
        'nama_belakang' : fields.String,
        'username' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_member, nama_depan, nama_belakang, username, email, password, status, created_at, updated_at):
        self.id_member = id_member
        self.nama_depan = nama_depan
        self.nama_belakang = nama_belakang
        self.username = username
        self.email = email
        self.password = password
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Member %r>' % self.id_member