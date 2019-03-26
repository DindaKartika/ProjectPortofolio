import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

class AdminResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def post(self):
        jwtClaim = get_jwt_claims()
        if jwtClaim['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('nama_depan', location = 'json', required = True)
            parser.add_argument('nama_belakang', location = 'json', required = True)
            parser.add_argument('username', location = 'json', required = True)
            parser.add_argument('email', location = 'json', required = True)
            parser.add_argument('password', location = 'json', required = True)
            args = parser.parse_args()

            args['status'] = "admin"
            args['created_at'] = datetime.datetime.now()
            args['updated_at'] = datetime.datetime.now()

            members = Member(None, args['nama_depan'], args['nama_belakang'], args['username'], args['email'], args['password'], args['status'], args['created_at'], args['updated_at'])
            db.session.add(members)
            db.session.commit()

            output = marshal(members, Member.response_field)

            return marshal(members, Member.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    def options(self):
        return {}, 200

api.add_resource(AdminResource, '/new')

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
                parser.add_argument('rp', type = int, location = 'args', default = 10)
                parser.add_argument('status', type=str, location = 'args')
                args = parser.parse_args()

                offside = (args['p'] * args['rp']) - args['rp']
                qry = Member.query

                if args['status'] is not None:
                    qry = qry.filter(Member.status.like("%"+args['status']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offside).all():
                    rows.append(marshal(row, Member.response_field))

                return rows, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
        else:
            qry = Member.query.get(id_member)
            member = marshal(qry, Member.response_field)
            details = DetailMember.query.filter(DetailMember.id_member == qry.id_member).first()
            member['detail'] = marshal(details, DetailMember.response_field)

            if qry is not None:
                return member, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_member):
        jwtClaims = get_jwt_claims()

        qry = Member.query.get(id_member)

        if jwtClaims['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('status', location = 'json')
            args = parser.parse_args()

            qry.status = args['status']
            
            qry.updated_at = datetime.datetime.now()

            db.session.commit()
            if qry is not None:
                return marshal(qry, Member.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    def options(self, id_member=None):
        return {}, 200


api.add_resource(MemberResource, '/member', '/member/<int:id_member>')

class TokoResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_toko = None):
        jwtClaims = get_jwt_claims()
        if id_toko == None:
            if jwtClaims['status'] == 'admin':
                parser = reqparse.RequestParser()
                parser.add_argument('p', type = int, location = 'args', default = 1)
                parser.add_argument('rp', type = int, location = 'args', default = 10)
                parser.add_argument('status', type=str, location = 'args')
                args = parser.parse_args()

                offside = (args['p'] * args['rp']) - args['rp']
                qry = Toko.query

                if args['status'] is not None:
                    qry = qry.filter(Toko.status.like("%"+args['status']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offside).all():
                    toko = marshal(row, Toko.response_field)
                    pemiliks = Member.query.filter(Member.id_member == row.id_member).first()
                    toko['pemilik'] = marshal(pemiliks, Member.response_field)
                    pengirimans = MetodePengiriman.query.filter(MetodePengiriman.id_metode_pengiriman == row.id_metode_pengiriman).first()
                    toko['pengiriman'] = marshal(pengirimans, MetodePengiriman.response_field)
                    rows.append(toko)

                return rows, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
        else:
            qry = Toko.query.get(id_toko)
            toko = marshal(qry, Toko.response_field)
            details = DetailToko.query.get(qry.id_toko)
            toko['detail'] = marshal(details, DetailToko.response_field)
            pemiliks = Member.query.filter(Member.id_member == qry.id_member).first()
            toko['pemilik'] = marshal(pemiliks, Member.response_field)
            pengirimans = MetodePengiriman.query.filter(MetodePengiriman.id_metode_pengiriman == qry.id_metode_pengiriman).first()
            toko['pengiriman'] = marshal(pengirimans, MetodePengiriman.response_field)

            if qry is not None:
                return toko, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_toko):
        jwtClaims = get_jwt_claims()

        qry = Toko.query.get(id_toko)

        if jwtClaims['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('status', location = 'json')
            args = parser.parse_args()

            qry.status = args['status']
            
            qry.updated_at = datetime.datetime.now()

            db.session.commit()
            if qry is not None:
                return marshal(qry, Toko.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    def options(self, id_toko=None):
        return {}, 200

api.add_resource(TokoResource, '/toko', '/toko/<int:id_toko>')

class BukuResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_buku = None):
        jwtClaims = get_jwt_claims()
        if id_buku == None:
            if jwtClaims['status'] == 'admin':
                parser = reqparse.RequestParser()
                parser.add_argument('p', type = int, location = 'args', default = 1)
                parser.add_argument('rp', type = int, location = 'args', default = 10)
                parser.add_argument('status', type=str, location = 'args')
                args = parser.parse_args()

                offside = (args['p'] * args['rp']) - args['rp']
                qry = Buku.query

                if args['status'] is not None:
                    qry = qry.filter(Buku.status.like("%"+args['status']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offside).all():
                    buku = marshal(row, Buku.response_field)
                    tokos = Toko.query.filter(Toko.id_toko == row.id_toko).first()
                    buku['toko'] = marshal(tokos, Toko.response_field)
                    rows.append(buku)

                return rows, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
        else:
            qry = Buku.query.get(id_buku)
            buku = marshal(qry, Buku.response_field)
            details = DetailBuku.query.get(qry.id_buku)
            buku['detail'] = marshal(details, DetailBuku.response_field)
            tokos = Toko.query.filter(Toko.id_toko == qry.id_buku).first()
            buku['shop'] = marshal(tokos, Toko.response_field)

            if qry is not None:
                return buku, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_buku):
        jwtClaims = get_jwt_claims()

        qry = Buku.query.get(id_buku)

        if jwtClaims['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('status', location = 'json')
            args = parser.parse_args()

            qry.status = args['status']
            
            qry.updated_at = datetime.datetime.now()

            db.session.commit()
            if qry is not None:
                return marshal(qry, Buku.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    def options(self, id_buku=None):
        return {}, 200

api.add_resource(BukuResource, '/buku', '/buku/<int:id_buku>')

class CartResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_cart = None):
        jwtClaims = get_jwt_claims()
        if id_cart == None:
            if jwtClaims['status'] == 'admin':
                parser = reqparse.RequestParser()
                parser.add_argument('p', type = int, location = 'args', default = 1)
                parser.add_argument('rp', type = int, location = 'args', default = 10)
                parser.add_argument('status', type=str, location = 'args')
                args = parser.parse_args()

                offside = (args['p'] * args['rp']) - args['rp']
                qry = Cart.query

                if args['status'] is not None:
                    qry = qry.filter(Cart.status.like("%"+args['status']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offside).all():
                    cart = marshal(row, Cart.response_field)
                    pembelis = Member.query.filter(Member.id_member == row.id_pembeli).first()
                    cart['pembeli'] = marshal(pembelis, Member.response_field)
                    rows.append(cart)

                return rows, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
        else:
            qry = Cart.query.get(id_cart)
            cart = marshal(qry, Cart.response_field)
            pembelis = Member.query.filter(Member.id_member == qry.id_pembeli).first()
            cart['pembeli'] = marshal(pembelis, Member.response_field)
            pembelians =  Pembelian.query.filter(Pembelian.id_cart == qry.id_cart).all()

            cart['pembelian'] = []
            for beli in pembelians:
                belis = marshal(beli, Pembelian.response_field)
                bukus = Buku.query.filter(Buku.id_buku == beli.id_buku).first()
                belis['buku'] = marshal(bukus, Buku.response_field)
                tokos = Toko.query.filter(Toko.id_toko == beli.id_toko).first()
                belis['toko'] = marshal(tokos, Toko.response_field)
                pengirimans = Toko.query.filter(MetodePengiriman.id_metode_pengiriman == beli.id_metode_pengiriman).first()
                belis['metode_pengiriman'] = marshal(pengirimans, MetodePengiriman.response_field)
                cart['pembelian'].append(belis)

            if qry is not None:
                return cart, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_cart):
        jwtClaims = get_jwt_claims()

        qry = Cart.query.get(id_cart)

        if jwtClaims['status'] == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('status', location = 'json')
            args = parser.parse_args()

            qry.status = args['status']
            
            qry.updated_at = datetime.datetime.now()

            db.session.commit()
            if qry is not None:
                return marshal(qry, Cart.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    def options(self, id_cart=None):
        return {}, 200


api.add_resource(CartResource, '/cart', '/cart/<int:id_cart>')

class TransaksiResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_transaksi = None):
        jwtClaims = get_jwt_claims()
        if id_transaksi == None:
            if jwtClaims['status'] == 'admin':
                parser = reqparse.RequestParser()
                parser.add_argument('p', type = int, location = 'args', default = 1)
                parser.add_argument('rp', type = int, location = 'args', default = 10)
                parser.add_argument('status', type=str, location = 'args')
                args = parser.parse_args()

                offside = (args['p'] * args['rp']) - args['rp']
                qry = Transaksi.query

                if args['status'] is not None:
                    qry = qry.filter(Transaksi.status.like("%"+args['status']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offside).all():
                    transaksi = marshal(row, Transaksi.response_field)
                    pembayarans = MetodePembayaran.query.filter(MetodePembayaran.id_metode_pembayaran == row.id_metode_pembayaran).first()
                    transaksi['pembayaran'] = marshal(pembayarans, MetodePembayaran.response_field)
                    rows.append(transaksi)

                return rows, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}
        else:
            qry = Transaksi.query.get(id_transaksi)
            transaksi = marshal(qry, Transaksi.response_field)
            pembayarans = MetodePembayaran.query.filter(MetodePembayaran.id_metode_pembayaran == qry.id_metode_pembayaran).first()
            transaksi['pembayaran'] = marshal(pembayarans, MetodePembayaran.response_field)

            if qry is not None:
                return transaksi, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_transaksi):
        jwtClaims = get_jwt_claims()

        qry = Transaksi.query.get(id_transaksi)

        if jwtClaims['status'] == 'admin':
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
        else:
            return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    def options(self, id_transaksi=None):
        return {}, 200

api.add_resource(TransaksiResource, '/transaksi', '/transaksi/<int:id_transaksi>')

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
        db.session.add(metode_pembayarans)
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
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()
        
        if args['metode_pembayaran'] is not None:
            qry.metode_pembayaran = args['metode_pembayaran']
        if args['instansi'] is not None:
            qry.instansi = args['instansi']
        if args['status'] is not None:
            qry.status = args['status']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, MetodePembayaran.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}

    def options(self, id_metode_pembayaran=None):
        return {}, 200


api.add_resource(MetodePembayaranResource, '/metode_pembayaran', '/metode_pembayaran/<int:id_metode_pembayaran>')

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
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()
        
        if args['metode'] is not None:
            qry.metode = args['metode']
        if args['kurir'] is not None:
            qry.kurir = args['kurir']
        if args['status'] is not None:
            qry.status = args['status']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, MetodePengiriman.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
        # else:
        #     return {'status' : 'ACCESS_DENIED', 'message' : 'ID false'}, 401, {'Content_type' : 'application/json'}


    def options(self, id_metode_pengiriman=None):
        return {}, 200

api.add_resource(MetodePengirimanResource, '/metode_pengiriman', '/metode_pengiriman/<int:id_metode_pengiriman>')