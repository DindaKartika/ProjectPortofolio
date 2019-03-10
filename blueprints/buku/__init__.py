import random, logging
from blueprints import db
from flask_restful import fields

from blueprints.toko import *

class Buku(db.Model):

    __tablename__ = "buku"

    id_buku = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_toko = db.Column(db.Integer)
    judul_buku = db.Column(db.String(255))
    harga = db.Column(db.Integer)
    kategori = db.Column(db.String(255))
    gambar = db.Column(db.String(255))
    kode_promo = db.Column(db.String(25))
    kondisi = db.Column(db.String(25))
    status = db.Column(db.String(50))
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # details = db.relationship('DetailBuku', backref = 'id_buku', lazy = True)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_buku' : fields.Integer,
        'id_toko' : fields.Integer,
        'judul_buku' : fields.String,
        'harga' : fields.Integer,
        'kategori' : fields.String,
        'gambar' : fields.String,
        'kode_promo' : fields.String,
        'kondisi' : fields.String,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_buku, id_toko, judul_buku, harga, kategori, gambar, kode_promo, kondisi, status, created_at, updated_at):
        self.id_buku = id_buku
        self.id_toko = id_toko
        self.judul_buku = judul_buku
        self.harga = harga
        self.kategori = kategori
        self.gambar = gambar
        self.kode_promo = kode_promo
        self.kondisi = kondisi
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Buku %r>' % self.id_buku