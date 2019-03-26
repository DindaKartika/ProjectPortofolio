import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_metode_pembayaran = Blueprint('metode_pembayaran', __name__)
api = Api(bp_metode_pembayaran)

class MetodePembayaranResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id_metode_pembayaran):
        qry = MetodePembayaran.query.get(id_metode_pembayaran)
        if qry is not None:
            return marshal(qry, MetodePembayaran.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self, id_metode_pembayaran=None):
        return {}, 200

api.add_resource(MetodePembayaranResource, '/<int:id_metode_pembayaran>')