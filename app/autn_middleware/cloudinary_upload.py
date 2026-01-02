from functools import wraps
from flask import request, jsonify, g
from ..config.cloudinary_config import cloudinary   # ensures config is loaded


def cloudinary_upload(field_name="image"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                if field_name not in request.files:
                    return jsonify({
                        "status": False,
                        "message": f"File missing in field '{field_name}'"
                    }), 400

                file = request.files[field_name]

                result = cloudinary.uploader.upload(file)

                # store for route access
                g.cloudinary_file = {
                    "url": result.get("secure_url"),
                    "public_id": result.get("public_id"),
                    "format": result.get("format"),
                    "resource_type": result.get("resource_type"),
                }

                return f(*args, **kwargs)

            except Exception as e:
                return jsonify({"status": False, "error": str(e)}), 500

        return wrapper
    return decorator
