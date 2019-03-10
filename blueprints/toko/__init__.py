import random, logging
from blueprints import db
from flask_restful import fields

class Toko(db.Model):

    __tablename__ = "toko"

    id_toko = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nama_toko = db.Column(db.String(255), unique = True)
    id_member = db.Column(db.Integer)
    id_metode_pengiriman = db.Column(db.Integer)
    rating = db.Column(db.Float)
    id_metode_pengiriman = db.Column(db.Integer)
    status = db.Column(db.String(50))
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # bukus = db.relationship('Buku', backref = 'id_toko', lazy = True)
    # details = db.relationship('DetailToko', backref = 'id_toko', lazy = True)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_toko' : fields.Integer,
        'nama_toko' : fields.String,
        'id_member' : fields.Integer,
        'rating' : fields.Float,
        'id_metode_pengiriman' : fields.Integer,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_toko, nama_toko, id_member, rating, id_metode_pengiriman, status, created_at, updated_at):
        self.id_toko = id_toko
        self.nama_toko = nama_toko
        self.id_member = id_member
        self.rating = rating
        self.id_metode_pengiriman = id_metode_pengiriman
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Toko %r>' % self.id_toko