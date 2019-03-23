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
            parser.add_argument('kategori', type=str, location = 'args')
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

            qry = qry.filter(Buku.status=='dijual')

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                buku = marshal(row, Buku.response_field)
                details = DetailBuku.query.filter(DetailBuku.id_buku == Buku.id_buku).first()
                buku['detail'] = marshal(details, DetailBuku.response_field)
                rows.append(buku)

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Buku.query.get(id_buku)
            if qry is not None:
                return marshal(qry, Buku.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self):
        return {}, 200


api.add_resource(BukuResource, '', '/<int:id_buku>')