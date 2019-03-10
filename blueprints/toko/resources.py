import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_toko = Blueprint('toko', __name__)
api = Api(bp_toko)

class TokoResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_toko):
        jwtClaim = get_jwt_claims()
        qry = Toko.query.get(id_toko)
        if qry is not None:
            return marshal(qry, Toko.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtClaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('nama_toko', location = 'json', required = True)
        parser.add_argument('id_metode_pengiriman', location = 'json', required = True)
        args = parser.parse_args()

        id_member = jwtClaim['id_member']
        args['rating_toko'] = 3
        args['status'] = "active"
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        tokos = Toko(None, args['nama_toko'], id_member, args['rating_toko'], args['id_metode_pengiriman'], args['status'], created_at, updated_at)
        db.session.add(tokos)
        db.session.commit()

        return marshal(tokos, Toko.response_field), 200, {'Content_type' : 'application/json'}

api.add_resource(TokoResource, '', '/<int:id_toko>')

class MyTokoResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_toko = None):
        jwtClaim = get_jwt_claims()
        if id_toko == None:
            qry = Toko.query
            if jwtClaim['status'] == 'admin':
                parser = reqparse.RequestParser()
                parser.add_argument('p', type = int, location = 'args', default = 1)
                parser.add_argument('rp', type = int, location = 'args', default = 5)
                parser.add_argument('nama_toko', type = str, location = 'args')
                parser.add_argument('id_member', type=str, location = 'args')
                parser.add_argument('status', type=str, location = 'args')
                args = parser.parse_args()

                offside = (args['p'] * args['rp']) - args['rp']
                
                if args['nama_toko'] is not None:
                    qry = qry.filter(Toko.nama_toko.like("%"+args['nama_toko']+"%"))
                if args['id_member'] is not None:
                    qry = qry.filter(Toko.id_member==args['id_member'])
                if args['status'] is not None:
                    qry = qry.filter(Toko.status.like("%"+args['status']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offside).all():
                    rows.append(marshal(row, Toko.response_field))

                return rows, 200, {'Content_type' : 'application/json'}
            elif jwtClaim['id_member'] == qry.id_member:
                qry = qry.filter(Toko.id_member==jwtClaim['id_member'])

                rows = []
                for row in qry.limit(args['rp']).offset(offside).all():
                    rows.append(marshal(row, Toko.response_field))

                return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Toko.query.get(id_toko)
            if qry is not None:
                return marshal(qry, Toko.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def delete(self):
        jwtClaim = get_jwt_claims()

        id_member = jwtClaim['id_member']

        qry = Toko.query.get(id_member)

        details = DetailToko.query.get(qry.id_toko)

        db.session.delete(details)
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtClaim = get_jwt_claims()

        id_member = jwtClaim['id_member']

        qry = Toko.query.get(id_member)

        parser = reqparse.RequestParser()
        parser.add_argument('nama_toko', location = 'json')
        parser.add_argument('rating_toko', location = 'json')
        parser.add_argument('id_metode_pengiriman', location = 'json')
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()
        
        if args['nama_toko'] is not None:
            qry.nama_toko = args['nama_toko']
        if args['rating_toko'] is not None:
            qry.rating_toko = args['rating_toko']
        if args['id_metode_pengiriman'] is not None:
            qry.id_metode_pengiriman = args['id_metode_pengiriman']
        if args['status'] is not None:
            qry.status = args['status']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Toko.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

api.add_resource(MyTokoResource, '/me')