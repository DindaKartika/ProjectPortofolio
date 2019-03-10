import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_member = Blueprint('member', __name__)
api = Api(bp_member)

class MemberResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_member = None):
        jwtClaims = get_jwt_claims()
        if id_member == None:
            if jwtClaims['status'] == 'admin':
                parser = reqparse.RequestParser()
                parser.add_argument('p', type = int, location = 'args', default = 1)
                parser.add_argument('rp', type = int, location = 'args', default = 5)
                parser.add_argument('username', type = str, location = 'args')
                parser.add_argument('status', type=str, location = 'args')
                args = parser.parse_args()

                offside = (args['p'] * args['rp']) - args['rp']
                qry = Member.query

                if args['username'] is not None:
                    qry = qry.filter(Member.username.like("%"+args['username']+"%"))
                if args['status'] is not None:
                    qry = qry.filter(Member.status.like("%"+args['status']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offside).all():
                    rows.append(marshal(row, Member.response_field))

                return rows, 200, {'Content_type' : 'application/json'}
            else:
                return 'Access Denied', 200, {'Content_type' : 'application/json'}
        else:
            if jwtClaims['id_member'] == id_member:
                qry = Member.query.get(id_member)
                if qry is not None:
                    return marshal(qry, Member.response_field), 200, {'Content_type' : 'application/json'}
                else:
                    return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_depan', location = 'json', required = True)
        parser.add_argument('nama_belakang', location = 'json', required = True)
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        args = parser.parse_args()

        args['status'] = "pembeli"
        args['created_at'] = datetime.datetime.now()
        args['updated_at'] = datetime.datetime.now()

        members = Member(None, args['nama_depan'], args['nama_belakang'], args['username'], args['email'], args['password'], args['status'], args['created_at'], args['updated_at'])
        db.session.add(members)
        db.session.commit()

        return marshal(members, Member.response_field), 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_member):
        jwtClaims = get_jwt_claims()

        qry = Member.query.get(id_member)

        if jwtClaims['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('status', location = 'json')
            args = parser.parse_args()

            qry.status = args['status']
        elif jwtClaims['id_member'] == id_member:
            parser = reqparse.RequestParser()
            parser.add_argument('nama_depan', location = 'json')
            parser.add_argument('nama_belakang', location = 'json')
            parser.add_argument('email', location = 'json')
            parser.add_argument('password', location = 'json')
            args = parser.parse_args()
            
            if args['nama_depan'] is not None:
                qry.nama_depan = args['nama_depan']
            if args['nama_belakang'] is not None:
                qry.nama_belakang = args['nama_belakang']
            if args['email'] is not None:
                qry.email = args['email']
            if args['password'] is not None:
                qry.password = args['password']
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
            
        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Member.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}


api.add_resource(MemberResource, '', '/<int:id_member>')

class MetodePembayaranResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_metode_pembayaran = None):
        # jwtClaim = get_jwt_claims()
        if id_metode_pembayaran == None:
            # if jwtClaim['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 10)
            parser.add_argument('metode_pembayaran', type = str, location = 'args')
            parser.add_argument('instansi', type = str, location = 'args')
            parser.add_argument('status', type = str, location = 'args')
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
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
        else:
            qry = MetodePembayaran.query.get(id_metode_pembayaran)
            if qry is not None:
                return marshal(qry, MetodePembayaran.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtClaim = get_jwt_claims()
        # if jwtClaim['status'] == 'admin':
        parser = reqparse.RequestParser()
        parser.add_argument('metode_pembayaran', location = 'json', required = True)
        parser.add_argument('instansi', location = 'json', required = True)
        args = parser.parse_args()

        args['status'] = "active"
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        metode_pembayarans = MetodePembayaran(None, args['metode_pembayaran'], args['instansi'], args['status'], created_at, updated_at)
        db.session.add(Metode_pembayarans)
        db.session.commit()

        return marshal(metode_pembayarans, MetodePembayaran.response_field), 200, {'Content_type' : 'application/json'}
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    @jwt_required
    def delete(self, id_metode_pembayaran):
        jwtClaim = get_jwt_claims()
        # if jwtClaim['status'] == 'admin':
        qry = MetodePembayaran.query.get(id_metode_pembayaran)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_metode_pembayaran):
        jwtClaim = get_jwt_claims()
        # if jwtClaim['status'] == 'admin':
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
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}


api.add_resource(MetodePembayaranResource, '', '/<int:id_metode_pembayaran>')

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