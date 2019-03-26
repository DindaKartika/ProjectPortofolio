import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required
import datetime

from . import *
from blueprints.buku import *
from blueprints.toko import *

bp_detail_buku = Blueprint('detail_buku', __name__)
api = Api(bp_detail_buku)

class DetailBukuResource(Resource):

    def __init__(self):
        pass

    def get(self, id_detail_buku = None):
        if id_detail_buku == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('penulis', type = str, location = 'args')
            parser.add_argument('penerbit', type = str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = DetailBuku.query

            if args['penulis'] is not None:
                qry = qry.filter(DetailBuku.penulis.like("%"+args['penulis']+"%"))
            if args['penerbit'] is not None:
                qry = qry.filter(DetailBuku.penerbit.like("%"+args['penerbit']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                Detail = marshal(row, DetailBuku.response_field)
                books = Buku.query.filter(Buku.id_buku == row.id_buku).first()
                Detail['book'] = marshal(books,Buku.response_field)
                shops = Toko.query.filter(Toko.id_toko == books.id_toko).first()
                Detail['shop'] = marshal(shops, Toko.response_field)
                rows.append(Detail)

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = DetailBuku.query.get(id_detail_buku)
            if qry is not None:
                return marshal(qry, DetailBuku.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_buku', location = 'json', required = True)
        parser.add_argument('isbn', location = 'json', required = True)
        parser.add_argument('penulis', location = 'json', required = True)
        parser.add_argument('penerbit', location = 'json', required = True)
        parser.add_argument('jumlah_halaman', location = 'json', required = True)
        parser.add_argument('sinopsis', location = 'json', required = True)
        parser.add_argument('stok', location = 'json', required = True)
        args = parser.parse_args()

        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        detail_bukus = DetailBuku(None, args['id_buku'], args['isbn'], args['penulis'], args['penerbit'], args['jumlah_halaman'], args['sinopsis'], args['stok'], created_at, updated_at)
        db.session.add(detail_bukus)
        db.session.commit()

        return marshal(detail_bukus, DetailBuku.response_field), 200, {'Content_type' : 'application/json'}

    def put(self, id_detail_buku):
        qry = DetailBuku.query.get(id_detail_buku)

        parser = reqparse.RequestParser()
        parser.add_argument('isbn', location = 'json')
        parser.add_argument('sinopsis', location = 'json')
        parser.add_argument('stok', location = 'json')
        args = parser.parse_args()
        
        if args['isbn'] is not None:
            qry.isbn = args['isbn']
        if args['sinopsis'] is not None:
            qry.sinopsis = args['sinopsis']
        if args['stok'] is not None:
            qry.stok = args['stok']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, DetailBuku.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self):
        return {}, 200


api.add_resource(DetailBukuResource, '', '/<int:id_detail_buku>')