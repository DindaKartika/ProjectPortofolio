import random, logging
from blueprints import db
from flask_restful import fields

from blueprints.pembelian import *

class Cart(db.Model):

    __tablename__ = "cart"

    id_cart = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_pembeli = db.Column(db.Integer)
    total_barang = db.Column(db.String(255))
    total_pembayaran = db.Column(db.Integer)
    status = db.Column(db.String(50))
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # transaksis = db.relationship('Transaksi', backref = 'id_cart', lazy = True)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_cart' : fields.Integer,
        'id_pembeli' : fields.Integer,
        'total_barang' : fields.String,
        'total_pembayaran' : fields.String,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_cart, id_pembeli, total_barang, total_pembayaran, status, created_at, updated_at):
        self.id_cart = id_cart
        self.id_pembeli = id_pembeli
        self.total_barang = total_barang
        self.total_pembayaran = total_pembayaran
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Cart %r>' % self.id_cart