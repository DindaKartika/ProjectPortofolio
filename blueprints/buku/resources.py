import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_buku = Blueprint('buku', __name__)
api = Api(bp_buku)

class BukuResource(Resource):

    def __init__(self):
        pass

    def get(self, id_buku = None):
        if id_buku == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('id_toko', type = str, location = 'args')
            parser.add_argument('judul_buku', type = str, location = 'args')
            parser.add_argument('kondisi', type = str, location = 'args')
            parser.add_argument('status', type=str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = buku.query

            if args['id_toko'] is not None:
                qry = qry.filter(Buku.id_toko=='id_toko')
            if args['judul_buku'] is not None:
                qry = qry.filter(Buku.judul_buku.like("%"+args['judul_buku']+"%"))
            if args['status'] is not None:
                qry = qry.filter(Buku.status.like("%"+args['status']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Buku.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = buku.query.get(id_buku)
            if qry is not None:
                return marshal(qry, Buku.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtClaim = get_jwt_claims()
        if jwtClaim['status'] == 'penjual':
            parser = reqparse.RequestParser()
            parser.add_argument('id_toko', location = 'json', required = True)
            parser.add_argument('judul_buku', location = 'json', required = True)
            parser.add_argument('harga', location = 'json', required = True)
            parser.add_argument('kategori', location = 'json', required = True)
            parser.add_argument('gambar', location = 'json', required = True)
            parser.add_argument('kode_promo', location = 'json')
            parser.add_argument('kondisi', location = 'json', required = True)
            args = parser.parse_args()

            args['status'] = "dijual"
            created_at = datetime.datetime.now()
            updated_at = datetime.datetime.now()

            bukus = buku(None, args['nama_depan'], args['nama_belakang'], args['username'], args['password'], args['id_alamat'], args['telepon'], args['status'], created_at, updated_at)
            db.session.add(bukus)
            db.session.commit()

            return marshal(bukus, Buku.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    @jwt_required
    def delete(self, id_buku):
        qry = Buku.query.get(id_buku)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_buku):
        qry = buku.query.get(id_buku)

        parser = reqparse.RequestParser()
        parser.add_argument('harga', location = 'json')
        parser.add_argument('kategori', location = 'json')
        parser.add_argument('gambar', location = 'json')
        parser.add_argument('kode_promo', location = 'json')
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()
        
        if args['harga'] is not None:
            qry.harga = args['harga']
        if args['kategori'] is not None:
            qry.kategori = args['kategori']
        if args['gambar'] is not None:
            qry.gambar = args['gambar']
        if args['kode_promo'] is not None:
            qry.kode_promo = args['kode_promo']
        if args['status'] is not None:
            qry.status = args['status']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Buku.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}


api.add_resource(BukuResource, '', '/<int:id_buku>')