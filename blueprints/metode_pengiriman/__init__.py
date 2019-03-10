import random, logging
from blueprints import db
from flask_restful import fields

class MetodePengiriman(db.Model):

    __tablename__ = "metode_pengiriman"

    id_metode_pengiriman = db.Column(db.Integer, primary_key = True, autoincrement = True)
    metode = db.Column(db.String(255))
    kurir = db.Column(db.String(255))
    status = db.Column(db.String(50))
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # tokos = db.relationship('Toko', backref = 'id_metode_pengiriman', lazy = True)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_metode_pengiriman' : fields.Integer,
        'metode' : fields.String,
        'kurir' : fields.String,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_metode_pengiriman, metode, kurir, status, created_at, updated_at):
        self.id_metode_pengiriman = id_metode_pengiriman
        self.metode = metode
        self.kurir = kurir
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<MetodePengiriman %r>' % self.id_metode_pengiriman