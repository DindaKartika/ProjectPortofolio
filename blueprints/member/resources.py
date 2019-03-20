import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime
from passlib.hash import sha256_crypt

from . import *

bp_member = Blueprint('member', __name__)
api = Api(bp_member)

class MemberResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        jwtClaims = get_jwt_claims()

        id_member = jwtClaims['id_member']

        qry = Member.query.get(id_member)
        member = marshal(qry, Member.response_field)
        details = DetailMember.query.get(qry.id_member)
        member['detail'] = marshal(details, DetailMember.response_field)

        if qry is not None:
            return member, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtClaims = get_jwt_claims()

        id_member = jwtClaims['id_member']

        qry = Member.query.get(id_member)
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
            
        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Member.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}


api.add_resource(MemberResource, '/me')

class MemberRegisterResource(Resource):

    def __init__(self):
        pass
    
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
        passwrd = sha256_crypt.encrypt(args['password'])

        members = Member(None, args['nama_depan'], args['nama_belakang'], args['username'], args['email'], passwrd, args['status'], args['created_at'], args['updated_at'])
        db.session.add(members)
        db.session.commit()

        return marshal(members, Member.response_field), 200, {'Content_type' : 'application/json'}

api.add_resource(MemberRegisterResource, '/register')