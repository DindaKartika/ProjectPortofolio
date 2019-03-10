import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_detail_member = Blueprint('detail_member', __name__)
api = Api(bp_detail_member)

class DetailMemberResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_detail_member = None):
        jwtClaims = get_jwt_claims()
        if id_detail_member == None:
            qry = DetailMember.query
            
            qry = qry.filter(DetailMember.id_member==jwtClaims['id_member'])

            rows = []
            for row in qry:
                rows.append(marshal(row, DetailMember.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = DetailMember.query.get(id_detail_member)
            if qry is not None:
                if jwtClaims['id_member'] == qry.id_member:
                    return marshal(qry, DetailMember.response_field), 200, {'Content_type' : 'application/json'}
                else:
                    return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtClaims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location = 'json', required = True)
        parser.add_argument('telepon', location = 'json', required = True)
        parser.add_argument('alamat_lengkap', location = 'json', required = True)
        parser.add_argument('kota', location = 'json', required = True)
        parser.add_argument('kecamatan', location = 'json', required = True)
        parser.add_argument('kode_pos', type = int, location = 'json', required = True)
        args = parser.parse_args()

        id_member = jwtClaims['id_member']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        details = DetailMember(None, id_member, args['nama'], args['telepon'], args['alamat_lengkap'], args['kota'], args['kecamatan'], args['kode_pos'], created_at, updated_at)
        db.session.add(details)
        db.session.commit()

        return marshal(details, DetailMember.response_field), 200, {'Content_type' : 'application/json'}

    @jwt_required
    def delete(self, id_detail_member):
        jwtClaims = get_jwt_claims()

        qry = DetailMember.query.get(id_detail_member)
        if jwtClaims['id_member'] == qry.id_member : 
            db.session.delete(qry)
            db.session.commit()

            if qry is not None:
                return 'Deleted', 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_detail_member):
        jwtClaims = get_jwt_claims()
        qry = DetailMember.query.get(id_detail_member)
        if jwtClaims['id_member'] == qry.id_member:
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
                return marshal(qry, DetailMember.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}


api.add_resource(DetailMemberResource, '/me', '/me/<int:id_detail_member>')