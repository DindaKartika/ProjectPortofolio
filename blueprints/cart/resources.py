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

    def get(self, id_cart = None):
        if id_cart == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('id_pembeli', type = str, location = 'args')
            parser.add_argument('status', type=str, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Cart.query

            if args['id_pembeli'] is not None:
                qry = qry.filter(Cart.id_pembeli.like("%"+args['id_pembeli']+"%"))
            if args['status'] is not None:
                qry = qry.filter(Cart.status.like("%"+args['status']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Cart.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Cart.query.get(id_cart)
            if qry is not None:
                return marshal(qry, Cart.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_pembeli', location = 'json', required = True)
        parser.add_argument('total_barang', location = 'json', required = True)
        parser.add_argument('total_pembayaran', location = 'json', required = True)
        args = parser.parse_args()

        args['status'] = "unfinished"
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        carts = cart(None, args['id_pembeli'], args['total_barang'], args['total_pembayaran'], args['status'], created_at, updated_at)
        db.session.add(carts)
        db.session.commit()

        return marshal(carts, Cart.response_field), 200, {'Content_type' : 'application/json'}

    def delete(self, id_cart):
        qry = Cart.query.get(id_cart)
        
        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def put(self, id_cart):
        qry = cart.query.get(id_cart)

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


api.add_resource(cartResource, '', '/<int:id_cart>')