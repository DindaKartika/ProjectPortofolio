import random, logging
from blueprints import db
from flask_restful import fields

class DetailMember(db.Model):

    __tablename__ = "detail_member"

    id_detail_member = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_member = db.Column(db.Integer)
    nama = db.Column(db.String(50))
    telepon = db.Column(db.String(20))
    alamat_lengkap = db.Column(db.String(255))
    kota = db.Column(db.String(50))
    kecamatan = db.Column(db.String(50))
    kode_pos = db.Column(db.Integer)
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_detail_member' : fields.Integer,
        'id_member' : fields.Integer,
        'nama' : fields.String,
        'telepon' : fields.String,
        'alamat_lengkap' : fields.String,
        'kota' : fields.String,
        'kecamatan' : fields.String,
        'kode_pos' : fields.Integer,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_detail_member, id_member, nama, telepon, alamat_lengkap, kota, kecamatan, kode_pos, created_at, updated_at):
        self.id_detail_member = id_detail_member
        self.id_member = id_member
        self.nama = nama
        self.telepon = telepon
        self.alamat_lengkap = alamat_lengkap
        self.kota = kota
        self.kecamatan = kecamatan
        self.kode_pos = kode_pos
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<DetailMember%r>' % self.id_detail_member