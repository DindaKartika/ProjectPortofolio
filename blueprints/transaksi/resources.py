import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_transaksi = Blueprint('transaksi', __name__)
api = Api(bp_transaksi)

class TransaksiResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_transaksi = None):
        jwtClaim = get_jwt_claims()
        
        if id_transaksi == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('status', type=str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']

            carts = Cart.query.filter(Cart.id_pembeli == jwtClaim['id_member']).all()

            rows = []
            for row in carts:
                qry = Transaksi.query.filter(Transaksi.id_cart == row.id_cart).first()
                rows.append(marshal(qry, Transaksi.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Transaksi.query.get(id_transaksi)
            if qry is not None:
                return marshal(qry, Transaksi.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_cart', location = 'json', required = True)
        parser.add_argument('id_metode_pembayaran', location = 'json', required = True)
        args = parser.parse_args()

        args['status'] = "staged"
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        transaksis = Transaksi(None, args['id_cart'], args['id_metode_pembayaran'], args['status'], created_at, updated_at)
        db.session.add(transaksis)
        db.session.commit()

        return marshal(transaksis, Transaksi.response_field), 200, {'Content_type' : 'application/json'}

api.add_resource(TransaksiResource, '', '/<int:id_transaksi>')