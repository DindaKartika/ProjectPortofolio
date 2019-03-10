import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required

from . import *

bp_pembelian = Blueprint('pembelian', __name__)
api = Api(bp_pembelian)

class PembelianResource(Resource):

    def __init__(self):
        pass

    def get(self, id_pembelian = None):
        if id_pembelian == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('id_pembeli', type = str, location = 'args')
            parser.add_argument('id_cart', type=str, location = 'args')
            parser.add_argument('id_toko', type=str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = pembelian.query

            if args['id_pembeli'] is not None:
                qry = qry.filter(pembelian.id_pembeli.like("%"+args['id_pembeli']+"%"))
            if args['id_cart'] is not None:
                qry = qry.filter(pembelian.id_cart.like("%"+args['id_cart']+"%"))
            if args['id_toko'] is not None:
                qry = qry.filter(pembelian.id_toko.like("%"+args['id_toko']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Pembelian.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Pembelian.query.get(id_pembelian)
            if qry is not None:
                return marshal(qry, Pembelian.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_pembeli', location = 'json', required = True)
        parser.add_argument('id_cart', location = 'json', required = True)
        parser.add_argument('id_buku', location = 'json', required = True)
        parser.add_argument('jumlah', location = 'json', required = True)
        parser.add_argument('total_harga', location = 'json', required = True)
        parser.add_argument('id_toko', location = 'json', required = True)
        parser.add_argument('id_metode_pengiriman', location = 'json', required = True)
        parser.add_argument('nomor_resi', location='json')
        args = parser.parse_args()

        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        pembelians = pembelian(None, args['id_pembeli'], args['id_cart'], args['id_buku'], args['jumlah'], args['total_harga'], args['id_toko'], args['id_metode_pengiriman'], args['nomor_resi'], created_at, updated_at)
        db.session.add(pembelians)
        db.session.commit()

        return marshal(pembelians, Pembelian.response_field), 200, {'Content_type' : 'application/json'}

    def delete(self, id_pembelian):
        qry = Pembelian.query.get(id_pembelian)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def put(self, id_pembelian):
        qry = Pembelian.query.get(id_pembelian)

        parser = reqparse.RequestParser()
        parser.add_argument('nomor_resi', location = 'json')
        args = parser.parse_args()
        
        qry.nomor_resi = args['nomor_resi']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Pembelian.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}


api.add_resource(PembelianResource, '', '/<int:id_pembelian>')