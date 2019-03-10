import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_metode_pengiriman = Blueprint('metode_pengiriman', __name__)
api = Api(bp_metode_pengiriman)

class MetodePengirimanResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_metode_pengiriman = None):
        jwtClaim = get_jwt_claims()
        if id_metode_pengiriman == None:
            # if jwtClaim['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 10)
            parser.add_argument('metode', type = str, location = 'args')
            parser.add_argument('kurir', type = str, location = 'args')
            parser.add_argument('status', type = str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = MetodePengiriman.query

            if args['metode'] is not None:
                qry = qry.filter(MetodePengiriman.metode.like("%"+args['metode']+"%"))
            if args['kurir'] is not None:
                qry = qry.filter(MetodePengiriman.kurir.like("%"+args['kurir']+"%"))
            if args['status'] is not None:
                qry = qry.filter(MetodePengiriman.status.like("%"+args['status']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, MetodePengiriman.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
        else:
            qry = MetodePengiriman.query.get(id_metode_pengiriman)
            if qry is not None:
                return marshal(qry, MetodePengiriman.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtClaim = get_jwt_claims()
        # if jwtClaim['status'] == 'admin':
        parser = reqparse.RequestParser()
        parser.add_argument('metode', location = 'json', required = True)
        parser.add_argument('kurir', location = 'json', required = True)
        args = parser.parse_args()

        args['status'] = "active"
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        metode_pengirimans = MetodePengiriman(None, args['metode'], args['kurir'], args['status'], created_at, updated_at)
        db.session.add(metode_pengirimans)
        db.session.commit()

        return marshal(metode_pengirimans, MetodePengiriman.response_field), 200, {'Content_type' : 'application/json'}
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    @jwt_required
    def delete(self, id_metode_pengiriman):
        jwtClaim = get_jwt_claims()
        # if jwtClaim['status'] == 'admin':
        qry = MetodePengiriman.query.get(id_metode_pengiriman)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_metode_pengiriman):
        jwtClaim = get_jwt_claims()
        # if jwtClaim['status'] == 'admin':
        qry = MetodePengiriman.query.get(id_metode_pengiriman)

        parser = reqparse.RequestParser()
        parser.add_argument('metode', location = 'json')
        parser.add_argument('kurir', location = 'json')
        args = parser.parse_args()
        
        if args['metode'] is not None:
            qry.metode = args['metode']
        if args['kurir'] is not None:
            qry.kurir = args['kurir']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, MetodePengiriman.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}


api.add_resource(MetodePengirimanResource, '', '/<int:id_metode_pengiriman>')