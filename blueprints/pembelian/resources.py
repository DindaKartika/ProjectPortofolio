import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_pembelian = Blueprint('pembelian', __name__)
api = Api(bp_pembelian)

class PembelianResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_pembelian):
        qry = Pembelian.query.get(id_pembelian)
        if qry is not None:
            return marshal(qry, Pembelian.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtClaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('id_buku', location = 'json', required = True)
        parser.add_argument('jumlah', location = 'json', required = True)
        parser.add_argument('id_metode_pengiriman', location = 'json', required = True)
        args = parser.parse_args()

        bukus = Buku.query.get(args['id_buku'])
        total_harga = int(args['jumlah']) * int(bukus.harga)
        args['nomor_resi'] = 0

        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        carts = Cart.query.filter(Cart.id_pembeli==jwtClaim['id_member']).filter(Cart.status == "unfinished").first()
        if carts is None:
            id_pembeli = jwtClaim['id_member']
            total_barang = args['jumlah']
            total_pembayaran = str(total_harga)
            status = "unfinished"

            cart_jadi = Cart(None, id_pembeli, total_barang, total_pembayaran, status, created_at, updated_at)
            db.session.add(cart_jadi)
            db.session.commit()
            carts = Cart.query.filter(Cart.id_pembeli==jwtClaim['id_member']).filter(Cart.status == "unfinished").first()

        else:

            carts.total_barang = int(carts.total_barang) + int(args['jumlah'])
            carts.total_pembayaran = str(carts.total_pembayaran + total_harga)
            db.session.commit()

        pembelians = Pembelian(None, carts.id_cart, args['id_buku'], args['jumlah'], total_harga, bukus.id_toko, args['id_metode_pengiriman'], args['nomor_resi'], created_at, updated_at)
        db.session.add(pembelians)
        db.session.commit()

        return marshal(pembelians, Pembelian.response_field), 200, {'Content_type' : 'application/json'}

    @jwt_required
    def delete(self, id_pembelian):
        qry = Pembelian.query.get(id_pembelian)

        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    def options(self):
        return {}, 200

api.add_resource(PembelianResource, '/me', '/me/<int:id_pembelian>')