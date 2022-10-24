from flask import request, jsonify, Blueprint

from flask_jwt_extended import ( jwt_required, create_access_token, get_jwt_identity, create_refresh_token )

from api import researcher

from . import mongo, TRACCAR_API_URL

user = Blueprint("user", __name__)

@user.route('')
@jwt_required()
def user_info():
    current_user = get_jwt_identity()
    if mongo.db is None:
        return jsonify(message="db error"), 500
    
    user_info = mongo.db.user.find_one({'email': current_user})
    
    if not user_info:
        return jsonify(message="no user data"), 400
    
    if user_info["role"] == "researcher":
        subjects = user_info["subjects"]
        researcher = ""
    else:
        subjects = []
        researcher = user_info["researcher"]

    data = {
        "name": user_info["name"],
        "email": user_info["email"],
        "role": user_info["role"],
        "device_id": user_info["device_id"],
        "subjects" : subjects,
        "researcher": researcher,
    }
    
    return jsonify(data=data), 200
  

@user.route('/refresh')
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    refresh_token = create_refresh_token(identity=current_user)
    
    return jsonify(access_token=access_token, refresh_token=refresh_token)