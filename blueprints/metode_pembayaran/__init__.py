import random, logging
from blueprints import db
from flask_restful import fields

class MetodePembayaran(db.Model):

    __tablename__ = "metode_pembayaran"

    id_metode_pembayaran = db.Column(db.Integer, primary_key = True, autoincrement = True)
    metode_pembayaran = db.Column(db.String(255))
    instansi = db.Column(db.String(255))
    status = db.Column(db.String(50))
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # transaksis = db.relationship('Transaksi', backref = 'id_metode_pembayaran', lazy = True)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_metode_pembayaran' : fields.Integer,
        'metode_pembayaran' : fields.String,
        'instansi' : fields.String,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_metode_pembayaran, metode_pembayaran, instansi, status, created_at, updated_at):
        self.id_metode_pembayaran = id_metode_pembayaran
        self.metode_pembayaran = metode_pembayaran
        self.instansi = instansi
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<MetodePembayaran %r>' % self.id_metode_pembayaran