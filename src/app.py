"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#get all members
@app.route('/members', methods=['GET'])
def get_all_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#get single member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    single_member = jackson_family.get_member(member_id)
    if single_member:
        return jsonify(single_member), 200
    else:
        return jsonify('Member not found'), 404
#add member
@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.json
    result = jackson_family.add_member(new_member)
    return jsonify(result), 200

#delete member 
@app.route('/member/<int:delete_id>', methods=['DELETE'])
def delete_member(delete_id):
    member_to_delete = jackson_family.get_member(delete_id)
    try:
        result = jackson_family.delete_member(delete_id)
    except:
        return 'ID not found', 400
    return jsonify(result), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
