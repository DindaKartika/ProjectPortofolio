from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from time import strftime
import json, logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

### Konfigurasi database

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/ecommerce'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'SFsieaaBsLEpecP675r243faM8oSB2hV'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days = 1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# db.create_all()

### Catch 404 errors with catch_all_404s = True

api = Api(app, catch_all_404s = True)

### Middleware

@app.after_request
def after_request(response):
    if request.method == 'GET':
        app.logger.warning("REQUEST LOG\t%s%s", json.dumps({'request' : request.args.to_dict(), 'response' : json.loads(response.data.decode('utf-8'))}), request.method)
    else:    
        app.logger.warning("REQUEST LOG\t%s%s", json.dumps({'request' : request.get_json(), 'response' : json.loads(response.data.decode('utf-8'))}), request.method)
    return response

jwt = JWTManager(app)
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

from blueprints.member.resources import bp_member
from blueprints.detail_member.resources import bp_detail_member
from blueprints.metode_pengiriman.resources import bp_metode_pengiriman
from blueprints.toko.resources import bp_toko
from blueprints.detail_toko.resources import bp_detail_toko
# from blueprints.buku.resources import bp_buku
# from blueprints.detail_buku.resources import bp_detail_buku
from blueprints.metode_pembayaran.resources import bp_metode_pembayaran
# from blueprints.cart.resources import bp_cart
# from blueprints.pembelian.resources import bp_pembelian
# from blueprints.transaction.resources import bp_transaction
# from blueprints.admin.resources import bp_admin
from blueprints.auth import bp_auth

app.register_blueprint(bp_member, url_prefix='/member')
app.register_blueprint(bp_detail_member, url_prefix='/detail_member')
app.register_blueprint(bp_metode_pengiriman, url_prefix='/metode_pengiriman')
app.register_blueprint(bp_toko, url_prefix='/toko')
app.register_blueprint(bp_detail_toko, url_prefix='/detail_toko')
# app.register_blueprint(bp_buku, url_prefix='/buku')
# app.register_blueprint(bp_detail_buku, url_prefix='/detail_buku')
app.register_blueprint(bp_metode_pembayaran, url_prefix='/metode_pembayaran')
# app.register_blueprint(bp_cart, url_prefix='/cart')
# app.register_blueprint(bp_pembelian, url_prefix='/pembelian')
# app.register_blueprint(bp_transaction, url_prefix='/transaksi')
# app.register_blueprint(bp_admin, url_prefix='/admin')
app.register_blueprint(bp_auth, url_prefix='/login')

db.create_all()