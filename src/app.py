"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
CORS(app)

# Añadir miembros iniciales manualmente
initial_members = [
    {
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    },
    {
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    },
    {
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    }
]

# Crear la instancia de la familia Jackson
jackson_family = FamilyStructure('Jackson')

for member in initial_members:
    jackson_family.add_member(member)

# Manejo de errores para respuestas JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generación del sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.json
    if not new_member or 'first_name' not in new_member or 'age' not in new_member or 'lucky_numbers' not in new_member:
        return jsonify({"error": "Invalid request body"}), 400
    jackson_family.add_member(new_member)
    return jsonify({"message": "Member added successfully"}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

# Este bloque se asegura de que la app se ejecute en modo debug y en el puerto correcto.
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
