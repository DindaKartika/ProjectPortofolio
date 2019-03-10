import random, logging
from blueprints import db
from flask_restful import fields

class DetailBuku(db.Model):

    __tablename__ = "detail_buku"

    id_detail_buku = db.Column(db.Integer, primary_key = True)
    id_buku = db.Column(db.Integer, unique = True)
    isbn = db.Column(db.String(255))
    penulis = db.Column(db.String(255))
    penerbit = db.Column(db.String(255))
    jumlah_halaman = db.Column(db.Integer)
    sinopsis = db.Column(db.String(2000))
    stok = db.Column(db.Integer)
    created_at= db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    response_field = {
        'id_detail_buku' : fields.Integer,
        'id_buku' : fields.Integer,
        'isbn' : fields.String,
        'penulis' : fields.String,
        'penerbit' : fields.String,
        'jumlah_halaman' : fields.String,
        'sinopsis' : fields.String,
        'stok' : fields.Integer,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id_detail_buku, id_buku, isbn, penulis, penerbit, jumlah_halaman, sinopsis, stok, created_at, updated_at):
        self.id_detail_buku = id_detail_buku
        self.id_buku = id_buku
        self.isbn = isbn
        self.penulis = penulis
        self.penerbit = penerbit
        self.jumlah_halaman = jumlah_halaman
        self.sinopsis = sinopsis
        self.stok = stok
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<DetailBuku %r>' % self.id_detail_buku