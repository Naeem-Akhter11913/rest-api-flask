from flask import jsonify,request

from pymongo.errors import PyMongoError

from bson import ObjectId

from ..schema.product__schema import ProductSchema

from ..extention import mongo

from datetime import datetime
from ..autn_middleware.auth__middleware import auth__required
# products ye ek table name hai aap yaha se kuch bhi de sakte hot database me is name ka collection ban jayega 

from flask_jwt_extended import jwt_required , get_jwt_identity , get_jwt


def create__product():
    try:
        data = request.get_json()
        
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
    user_id = get_jwt_identity()   # <-- user _id
    claims = get_jwt() 
    print(user_id)
    try:
         products = mongo.db.ProductSchema.find()
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


def find__one__collection(id):
     try:
          data__to__be__update = request.get_json()
          print(id)
          isExists = mongo.db.ProductSchema.find_one({"_id": ObjectId(id)})

          if not isExists:
               return jsonify({
                    'status':False,
                    'message':'Opps! You are not allowed! '
               }), 401
          mongo.db.ProductSchema.update_one({"_id": ObjectId(id)}, {'$set': data__to__be__update})
          return jsonify({
               "status": True,
               "Message": "Product get successfully!"
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
     
