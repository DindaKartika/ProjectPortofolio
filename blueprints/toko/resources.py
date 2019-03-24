import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *
from blueprints.toko import *
from blueprints.member import *
from blueprints.cart import *

bp_toko = Blueprint('toko', __name__)
api = Api(bp_toko)

class TokoResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_toko):
        qry = Toko.query.get(id_toko)
        tokos = marshal(qry, Toko.response_field)
        details = DetailToko.query.get(id_toko)
        tokos['detail'] = marshal(details, DetailToko.response_field)
        
        if qry is not None:
            return tokos, 200, {'Content_type' : 'application/json'}
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
        
    def options(self):
        return {}, 200

api.add_resource(TokoResource, '', '/<int:id_toko>')

class MyTokoResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        jwtClaim = get_jwt_claims()

        qry = Toko.query
        id_members = jwtClaim['id_member']
        qry = Toko.query.filter(Toko.id_member == id_members).one()

        tokos = marshal(qry, Toko.response_field)
        details = DetailToko.query.get(qry.id_toko)
        tokos['detail'] = marshal(details, DetailToko.response_field)

        if tokos is not None:
            return tokos, 200, {'Content_type' : 'application/json'}
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

    def options(self):
        return {}, 200

api.add_resource(MyTokoResource, '/me')

class BukuTokoResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_buku = None):
        jwtClaim = get_jwt_claims()
        if jwtClaim['status'] == 'penjual':
            if id_buku == None:
                parser = reqparse.RequestParser()
                parser.add_argument('p', type = int, location = 'args', default = 1)
                parser.add_argument('rp', type = int, location = 'args', default = 5)
                parser.add_argument('judul_buku', type = str, location = 'args')
                parser.add_argument('kondisi', type = str, location = 'args')
                parser.add_argument('kategori', type=str, location = 'args')
                parser.add_argument('status', type=str, location = 'args')
                args = parser.parse_args()

                offside = (args['p'] * args['rp']) - args['rp']
                qry = Buku.query

                tokos = Toko.query.filter(Toko.id_member == jwtClaim['id_member']).first()
                qry = qry.filter(Buku.id_toko==tokos.id_toko).all()

                if args['judul_buku'] is not None:
                    qry = qry.filter(Buku.judul_buku.like("%"+args['judul_buku']+"%"))
                if args['kondisi'] is not None:
                    qry = qry.filter(Buku.kondisi.like("%"+args['kondisi']+"%"))
                if args['kategori'] is not None:
                    qry = qry.filter(Buku.kategori.like("%"+args['kategori']+"%"))
                if args['status'] is not None:
                    qry = qry.filter(Buku.status.like("%"+args['status']+"%"))

                rows = []
                for row in qry:
                    rows.append(marshal(row, Buku.response_field))

                return rows, 200, {'Content_type' : 'application/json'}
            else:
                qry = buku.query.get(id_buku)
                if qry is not None:
                    return marshal(qry, Buku.response_field), 200, {'Content_type' : 'application/json'}
                else:
                    return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtClaim = get_jwt_claims()

        id_member = jwtClaim['id_member']
        tokos = Toko.query.filter(Toko.id_member == id_member).first()
        if tokos is not None:
            id_tokos = tokos.id_toko

            parser = reqparse.RequestParser()
            parser.add_argument('judul_buku', location = 'json', required = True)
            parser.add_argument('harga', location = 'json', required = True)
            parser.add_argument('kategori', location = 'json', required = True)
            parser.add_argument('gambar', location = 'json', required = True)
            parser.add_argument('kode_promo', location = 'json')
            parser.add_argument('kondisi', location = 'json', required = True)
            args = parser.parse_args()

            args['id_toko'] = id_tokos

            args['status'] = "dijual"
            created_at = datetime.datetime.now()
            updated_at = datetime.datetime.now()

            bukus = Buku(None, args['id_toko'], args['judul_buku'], args['harga'], args['kategori'], args['gambar'], args['kode_promo'], args['kondisi'], args['status'], created_at, updated_at)
            db.session.add(bukus)

            member = Member.query.filter(Member.id_member == id_member).first()
            member.status = 'penjual'

            db.session.commit()

            return marshal(bukus, Buku.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'Bukan Penjual'}, 404, {'Content_type' : 'application/json'}


    @jwt_required
    def delete(self, id_buku):
        qry = Buku.query.get(id_buku)
        details = DetailBuku.query.get(id_buku)
        
        db.session.delete(details)
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_buku):
        qry = Buku.query.get(id_buku)

        parser = reqparse.RequestParser()
        parser.add_argument('harga', location = 'json')
        parser.add_argument('kategori', location = 'json')
        parser.add_argument('gambar', location = 'json')
        parser.add_argument('kode_promo', location = 'json')
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()
        
        if args['harga'] is not None:
            qry.harga = args['harga']
        if args['kategori'] is not None:
            qry.kategori = args['kategori']
        if args['gambar'] is not None:
            qry.gambar = args['gambar']
        if args['kode_promo'] is not None:
            qry.kode_promo = args['kode_promo']
        if args['status'] is not None:
            qry.status = args['status']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Buku.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self):
        return {}, 200


api.add_resource(BukuTokoResource, '/buku', '/buku/<int:id_buku>')

class PembelianTokoResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_pembelian = None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 10)
        args = parser.parse_args()

        jwtClaim = get_jwt_claims()

        tokos = Toko.query.filter(Toko.id_member == jwtClaim['id_member']).first()

        offside = (args['p'] * args['rp']) - args['rp']
        qry = Pembelian.query

        qry = qry.filter(Pembelian.id_toko==tokos.id_toko)

        rows = []
        for row in qry.limit(args['rp']).offset(offside).all():
            penjualan = marshal(row, Pembelian.response_field)
            carts = Cart.query.filter(Cart.id_cart == row.id_cart).filter(Cart.status=='unfinished').first()
            penjualan['cart'] = marshal(carts, Cart.response_field)
            pembeli = Member.query.filter(Member.id_member == carts.id_pembeli).first()
            penjualan['pembeli'] = marshal(pembeli, Member.response_field)
            bukus = Buku.query.filter(Buku.id_buku == row.id_buku).first()
            penjualan['buku'] = marshal(bukus, Buku.response_field)
            rows.append(penjualan)

        return rows, 200, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self, id_pembelian):
        qry = Pembelian.query.get(id_pembelian)

        parser = reqparse.RequestParser()
        parser.add_argument('nomor_resi', location = 'json')
        args = parser.parse_args()
        
        qry.nomor_resi = args['nomor_resi']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Pembelian.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self):
        return {}, 200


api.add_resource(PembelianTokoResource, '/penjualan', '/penjualan/<int:id_pembelian>')