import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required
import datetime

from . import *

bp_detail_buku = Blueprint('detail_buku', __name__)
api = Api(bp_detail_buku)

class DetailBukuResource(Resource):

    def __init__(self):
        pass
    
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


api.add_resource(DetailBukuResource, '', '/<int:id_detail_buku>')