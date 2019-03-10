import random, logging
from blueprints import db
from flask_restful import fields

class AlamatToko(db.Model):

    __tablename__ = "alamat_toko"

    id_alamat_toko = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_toko = db.Column(db.Integer, unique = True)
    alamat_lengkap = db.Column(db.String(255))
    kota = db.Column(db.String(50))
    kecamatan = db.Column(db.String(50))
    kode_pos = db.Column(db.Integer)
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_alamat_toko' : fields.Integer,
        'id_toko' : fields.Integer,
        'alamat_lengkap' : fields.String,
        'kota' : fields.String,
        'kecamatan' : fields.String,
        'kode_pos' : fields.Integer,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_alamat_toko, id_toko, alamat_lengkap, kota, kecamatan, kode_pos, created_at, updated_at):
        self.id_alamat_toko = id_alamat_toko
        self.id_toko = id_toko
        self.alamat_lengkap = alamat_lengkap
        self.kota = kota
        self.kecamatan = kecamatan
        self.kode_pos = kode_pos
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<AlamatToko%r>' % self.id_alamat_toko