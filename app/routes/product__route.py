from flask import Blueprint

from ..controllers.product__controller import create__product, findAll__product, find__one__and__update__collection, find__one__collection

product_bp = Blueprint("product", __name__)

product_bp.route('/add', methods=["POST"])(create__product)
product_bp.route('/get',methods=['GET'])(findAll__product)
product_bp.route('/update/<id>',methods=['PUT'])(find__one__and__update__collection)
product_bp.route('/get-one/<id>',methods=['GET'])(find__one__collection)