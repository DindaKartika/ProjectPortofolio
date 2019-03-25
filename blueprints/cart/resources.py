import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *
from blueprints.pembelian import *

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        jwtClaim = get_jwt_claims()
        id_pembelis = jwtClaim['id_member']

        qry = Cart.query.filter(Cart.id_pembeli == id_pembelis).filter(Cart.status == 'unfinished').first()
        cart = marshal(qry, Cart.response_field)

        pembelians =  Pembelian.query.filter(Pembelian.id_cart == qry.id_cart).all()

        rows = []
        for row in pembelians:
            cart['pembelian'] = marshal(pembelians, Pembelian.response_field)
            rows.append(cart)

        if qry is not None:
            return cart, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self):
        return {}, 200

api.add_resource(CartResource, '/me')

class CartAllResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        jwtClaim = get_jwt_claims()
        id_pembelis = jwtClaim['id_member']

        qry = Cart.query.filter(Cart.id_pembeli == id_pembelis).all()

        rows = []
        for row in qry:
            carts = marshal(row, Cart.response_field)
            rows.append(carts)

        if qry is not None:
            return qry, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self):
        return {}, 200

api.add_resource(CartAllResource, '/all')