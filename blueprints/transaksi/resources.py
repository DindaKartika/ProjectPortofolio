import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required

from . import *

bp_transaksi = Blueprint('transaksi', __name__)
api = Api(bp_transaksi)

class TransaksiResource(Resource):

    def __init__(self):
        pass

    def get(self, id_transaksi = None):
        if id_transaksi == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('status', type=str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Transaksi.query

            if args['status'] is not None:
                qry = qry.filter(Transaksi.status.like("%"+args['status']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Transaksi.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Transaksi.query.get(id_transaksi)
            if qry is not None:
                return marshal(qry, Transaksi.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
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

    def delete(self, id_transaksi):
        qry = Transaksi.query.get(id_transaksi)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def put(self, id_transaksi):
        qry = Transaksi.query.get(id_transaksi)

        parser = reqparse.RequestParser()
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()
        
        qry.status = args['status']
        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Transaksi.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}


api.add_resource(TransaksiResource, '', '/<int:id_transaksi>')