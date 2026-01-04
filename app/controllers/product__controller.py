from flask import jsonify,request

from pymongo.errors import PyMongoError

from bson import ObjectId
from flask import g
from bson.json_util import dumps, loads

from ..schema.product__schema import ProductSchema

from ..extention import mongo

from datetime import datetime
from ..autn_middleware.auth__middleware import auth__required
from ..autn_middleware.cloudinary_upload import cloudinary_upload
from ..utils.serialize_doc import serialize_doc
# products ye ek table name hai aap yaha se kuch bhi de sakte hot database me is name ka collection ban jayega 

from flask_jwt_extended import jwt_required , get_jwt_identity , get_jwt

@auth__required
@jwt_required()
@cloudinary_upload("image")
def create__product():
    name = request.form.get("name")
    price = request.form.get("price")
    desc = request.form.get("desc")
    user_id = get_jwt_identity()
    
    image = g.cloudinary_file
    try:
        data = {
            "name": name,
            "price": price,
            "desc": desc,
            "image_url": image["url"],
        }
        name = data.get("name")
        if not name:
            return jsonify({
                "status": False,
                "message": "Field 'name' is required"
            }), 400
        isExists = mongo.db.ProductSchema.find_one({"name": data.get('name')})

        if isExists:
            return jsonify({
                "status": False,
                "message": "You are trying to push same product!",
            }), 409

        now = datetime.utcnow()

        data["createdAt"] = now
        data["updatedAt"] = now
        data["userId"] = user_id

        mongo.db.ProductSchema.insert_one(data)
        return jsonify({"status": True, "message": "Data inserted successfully"}), 200
    except PyMongoError as e:
        return jsonify({
            "status": False,
            "message": f"Database error: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "status": False,
            "message": f"Something went wrong {str(e)}"
        }),500

@jwt_required()
@auth__required
def findAll__product():
    try:
         user_id = get_jwt_identity()
         products = mongo.db.ProductSchema.find({"userId":user_id})
        #  json__data__converted = serialize_doc(products)
         
         return jsonify({
            "status": True,
            "message": "All data fetched successfully",
            "data": products
         }), 200
    except PyMongoError as e:
            return jsonify({
                "status": False,
                "message": f"Database error: {str(e)}"
            }), 500
    except Exception as e:
        jsonify({
            "status": False,
            "message": f"Something went wrong {str(e)}"
        })

@jwt_required()
@auth__required
def find__one__and__update__collection(id):
     try:
          data__to__be__update = request.get_json()
          isExists = mongo.db.ProductSchema.find_one({"_id": ObjectId(id)})

          if not isExists:
               return jsonify({
                    'status':False,
                    'message':'Opps! You are not allowed! '
               }), 401
          mongo.db.ProductSchema.update_one({"_id": ObjectId(id)}, {'$set': data__to__be__update})
          return jsonify({
               "status": True,
               "Message": "Product Updated successfully!"
          }), 200
     except PyMongoError as e:
            return jsonify({
                "status": False,
                "message": f"Database error: {str(e)}"
            }), 500
     except Exception as e:
            return jsonify({
                "status": False,
                "message": f"Something went wrong {str(e)}"
            })
@jwt_required()
@auth__required
def find__one__collection(id):
     try:
          user_id = get_jwt_identity()
          isExists = mongo.db.ProductSchema.find_one({"_id": ObjectId(id),"userId":user_id})
          json__converted = serialize_doc(isExists)
          return jsonify({
                "status": True,
                "data": json__converted,
                "message": "Data fetch successfully"
            }), 200
     except PyMongoError as e:
          return jsonify({
                "status": False,
                "message": f"Database error: {str(e)}"
            }), 500
     except Exception as e:
          return jsonify({
                "status": False,
                "message": f"Something went wrong {str(e)}"
            })