import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *
from blueprints.toko import *
from blueprints.metode_pengiriman import *

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
            parser.add_argument('kategori', type=str, location = 'args')
            parser.add_argument('penerbit', type=str, location = 'args')
            parser.add_argument('penulis', type=str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Buku.query

            if args['id_toko'] is not None:
                qry = qry.filter(Buku.id_toko=='id_toko')
            if args['judul_buku'] is not None:
                qry = qry.filter(Buku.judul_buku.like("%"+args['judul_buku']+"%"))
            if args['kondisi'] is not None:
                qry = qry.filter(Buku.kondisi.like("%"+args['kondisi']+"%"))
            if args['kategori'] is not None:
                qry = qry.filter(Buku.kategori.like("%"+args['kategori']+"%"))
            if args['penerbit'] is not None:
                qry = qry.filter(Buku.penerbit.like("%"+args['penerbit']+"%"))
            if args['penulis'] is not None:
                qry = qry.filter(Buku.penulis.like("%"+args['penulis']+"%"))

            qry = qry.filter(Buku.status=='dijual')

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                buku = marshal(row, Buku.response_field)
                details = DetailBuku.query.filter(DetailBuku.id_buku == row.id_buku).first()
                buku['detail'] = marshal(details, DetailBuku.response_field)
                tokos = Toko.query.filter(Toko.id_toko == row.id_toko).first()
                buku['shop'] = marshal(tokos, Toko.response_field)
                rows.append(buku)

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Buku.query.get(id_buku)
            buku = marshal(qry, Buku.response_field)
            details = DetailBuku.query.filter(DetailBuku.id_buku == qry.id_buku).first()
            buku['detail'] = marshal(details, DetailBuku.response_field)
            tokos = Toko.query.filter(Toko.id_toko == qry.id_toko).first()
            buku['shop'] = marshal(tokos, Toko.response_field)
            methods = MetodePengiriman.query.filter(MetodePengiriman.id_metode_pengiriman==Toko.id_metode_pengiriman).first()
            buku['kurir'] = marshal(methods, MetodePengiriman.response_field)
            if qry is not None:
                return buku, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self):
        return {}, 200


api.add_resource(BukuResource, '', '/<int:id_buku>')