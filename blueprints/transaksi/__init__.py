import random, logging
from blueprints import db
from flask_restful import fields

from blueprints.cart import *

class Transaksi(db.Model):

    __tablename__ = "transaksi"

    id_transaksi = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_cart = db.Column(db.Integer)
    id_metode_pembayaran = db.Column(db.Integer)
    status = db.Column(db.String(50), unique = True)
    created_at= db.Column(db.DateTime, unique = True)
    updated_at = db.Column(db.DateTime, unique = True)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_transaksi' : fields.Integer,
        'id_cart' : fields.String,
        'id_metode_pembayaran' : fields.String,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_transaksi, id_cart, id_metode_pembayaran, status, created_at, updated_at):
        self.id_transaksi = id_transaksi
        self.id_cart = id_cart
        self.id_metode_pembayaran = id_metode_pembayaran
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Transaksi %r>' % self.id_transaksi