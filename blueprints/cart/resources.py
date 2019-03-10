import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required

from . import *

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):

    def __init__(self):
        pass

    def get(self, id_cart):
        qry = Cart.query.get(id_cart)
        qry = marshal(qry, Cart.response_field)

        pembelians =  Pembelian.query.filter(Pembelian.id_cart == qry.id_cart).all()

        rows = []
        for row in pembelians:
            qry['pembelian'] = marshal(row, Pembelian.response_field)
            rows.append(qry)

        if qry is not None:
            return rows, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

api.add_resource(CartResource, '/<int:id_cart>')