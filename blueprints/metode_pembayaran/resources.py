import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required

from . import *

bp_metode_pembayaran = Blueprint('metode_pembayaran', __name__)
api = Api(bp_metode_pembayaran)

class MetodePembayaranResource(Resource):

    def __init__(self):
        pass

    def get(self, id_metode_pembayaran = None):
        if id_metode_pembayaran == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('metode_pembayaran', type = str, location = 'args')
            parser.add_argument('instansi', type = str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = MetodePembayaran.query

            if args['metode_pembayaran'] is not None:
                qry = qry.filter(MetodePembayaran.metode_pembayaran.like("%"+args['metode_pembayaran']+"%"))
            if args['instansi'] is not None:
                qry = qry.filter(MetodePembayaran.instansi.like("%"+args['instansi']+"%"))
            if args['status'] is not None:
                qry = qry.filter(MetodePembayaran.status.like("%"+args['status']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, MetodePembayaran.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = MetodePembayaran.query.get(id_metode_pembayaran)
            if qry is not None:
                return marshal(qry, MetodePembayaran.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('metode_pembayaran', location = 'json', required = True)
        parser.add_argument('instansi', location = 'json', required = True)
        parser.add_argument('telepon', location = 'json', required = True)
        args = parser.parse_args()

        args['status'] = "pembeli"
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        metode_pembayarans = MetodePembayaran(None, args['nama_depan'], args['metode_pembayaran'], args['instansi'], args['status'], created_at, updated_at)
        db.session.add(metode_pembayarans)
        db.session.commit()

        return marshal(metode_pembayaran, MetodePembayaran.response_field), 200, {'Content_type' : 'application/json'}

    def delete(self, id_metode_pembayaran):
        qry = MetodePembayaran.query.get(id_metode_pembayaran)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def put(self, id_metode_pembayaran):
        qry = MetodePembayaran.query.get(id_metode_pembayaran)

        parser = reqparse.RequestParser()
        parser.add_argument('metode_pembayaran', location = 'json')
        parser.add_argument('instansi', location = 'json')
        args = parser.parse_args()
        
        if args['metode_pembayaran'] is not None:
            qry.metode_pembayaran = args['metode_pembayaran']
        if args['instansi'] is not None:
            qry.instansi = args['instansi']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, MetodePembayaran.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}


api.add_resource(MetodePembayaranResource, '', '/<int:id_metode_pembayaran>')