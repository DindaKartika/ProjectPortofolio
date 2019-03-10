import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime
from datetime import timedelta

from . import *

bp_detail_toko = Blueprint('detail_toko', __name__)
api = Api(bp_detail_toko)

class DetailTokoResource(Resource):

    def __init__(self):
        pass

    # @jwt_required
    # def get(self, id_detail_toko = None):
    #     if id_detail_toko == None:
    #         jwtClaim = get_jwt_claims()
    #         if jwtClaim['status'] == 'admin':
    #             parser = reqparse.RequestParser()
    #             parser.add_argument('p', type = int, location = 'args', default = 1)
    #             parser.add_argument('rp', type = int, location = 'args', default = 5)
    #             parser.add_argument('kota', type = str, location = 'args')
    #             parser.add_argument('id_toko', type = str, location = 'args')
    #             args = parser.parse_args()

    #             offside = (args['p'] * args['rp']) - args['rp']
    #             qry = DetailToko.query

    #             if args['kota'] is not None:
    #                 qry = qry.filter(DetailToko.kota.like("%"+args['kota']+"%"))
    #             if args['id_toko'] is not None:
    #                 qry = qry.filter(DetailToko.id_toko.like("%"+args['id_toko']+"%"))

    #             rows = []
    #             for row in qry.limit(args['rp']).offset(offside).all():
    #                 rows.append(marshal(row, DetailToko.response_field))

    #             return rows, 200, {'Content_type' : 'application/json'}
    #         else:
    #             return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
    #     else:
    #         qry = DetailToko.query.get(id_detail_toko)
    #         if qry is not None:
    #             return marshal(qry, DetailToko.response_field), 200, {'Content_type' : 'application/json'}
    #         else:
    #             return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtClaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('alamat_lengkap', location = 'json', required = True)
        parser.add_argument('kota', location = 'json', required = True)
        parser.add_argument('kecamatan', location = 'json', required = True)
        parser.add_argument('kode_pos', type = int, location = 'json', required = True)
        args = parser.parse_args()

        id_member = jwtClaim['id_member']
        tokos = Toko.query.get(id_member)
        args['id_toko'] = tokos.id_toko

        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        details = DetailToko(None, args['id_toko'], args['alamat_lengkap'], args['kota'], args['kecamatan'], args['kode_pos'], created_at, updated_at)
        db.session.add(details)
        db.session.commit()

        return marshal(details, DetailToko.response_field), 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtClaim = get_jwt_claims()

        id_member = jwtClaim['id_member']
        tokos = Toko.query.get(id_member)

        qry = DetailToko.query.get(tokos.id_toko)

        parser = reqparse.RequestParser()
        parser.add_argument('alamat_lengkap', location = 'json')
        parser.add_argument('kota', location = 'json')
        parser.add_argument('kecamatan', location = 'json')
        parser.add_argument('kode_pos', type = int, location = 'json')
        args = parser.parse_args()
        
        if args['alamat_lengkap'] is not None:
            qry.alamat_lengkap = args['alamat_lengkap']
        if args['kota'] is not None:
            qry.kota = args['kota']
        if args['kecamatan'] is not None:
            qry.kecamatan = args['kecamatan']
        if args['kode_pos'] is not None:
            qry.kode_pos = args['kode_pos']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, DetailToko.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}


api.add_resource(DetailTokoResource, '')