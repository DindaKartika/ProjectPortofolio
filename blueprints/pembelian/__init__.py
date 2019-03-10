import random, logging
from blueprints import db
from flask_restful import fields

from blueprints.cart import *

class Pembelian(db.Model):

    __tablename__ = "pembelian"

    id_pembelian = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_pembeli = db.Column(db.Integer)
    id_cart = db.Column(db.Integer)
    id_buku = db.Column(db.Integer)
    jumlah = db.Column(db.String(255), unique = True)
    total_harga = db.Column(db.String(255))
    id_toko = db.Column(db.Integer)
    id_metode_pengiriman = db.Column(db.Integer)
    nomor_resi = db.Column(db.String(50))
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_pembelian' : fields.Integer,
        'id_pembeli' : fields.String,
        'id_cart' : fields.String,
        'id_buku' : fields.String,
        'jumlah' : fields.String,
        'total_harga' : fields.String,
        'id_toko' : fields.Integer,
        'id_metode_pengiriman' : fields.String,
        'nomor_resi' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_pembelian, id_pembeli, id_cart, id_buku, jumlah, total_harga, id_toko, id_metode_pengiriman, nomor_resi, created_at, updated_at):
        self.id_pembelian = id_pembelian
        self.id_pembeli = id_pembeli
        self.id_cart = id_cart
        self.id_buku = id_buku
        self.jumlah = jumlah
        self.total_harga = total_harga
        self.id_toko = id_toko
        self.id_metode_pengiriman = id_metode_pengiriman
        self.nomor_resi = nomor_resi
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Pembelian %r>' % self.id_pembelian