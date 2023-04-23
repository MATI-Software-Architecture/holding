from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from app import struct_collection

structs = Blueprint(
    'structs_manager', __name__, url_prefix='/config/struct'
)


@structs.route('/mandatory', methods=['POST'])
def mandatory_fields():
    """
    Create mandatory fields key in the collection
    """
    data = request.json
    fields = data.get('fields')
    if fields and isinstance(fields, list):
        data['_id'] = 'mandatory'
        result = struct_collection.update_one(
            {'_id': 'mandatory'},
            {"$set": data},
            upsert=True
        )
        if result.acknowledged:
            return jsonify({'message': 'Document upserted'}), 201
    return jsonify({'error': 'fields must be a list with key mandatory'}), 400


@structs.route('/mandatory', methods=['GET'])
def read_mandatory():
    """
    Read mandatory fields from the collection
    """
    document = struct_collection.find_one(
        {'_id': 'mandatory'},
        {'_id': 0, 'fields': 1}
    )
    if document:
        return jsonify(document), 200
    return jsonify({'error': 'Document not found'}), 404


@structs.route('/mapping/<company>', methods=['POST'])
def update_mapping(company):
    """
    Update a single mapping in the collection by ID
    """
    data = request.json
    mapping = data.get('mapping')
    if mapping and isinstance(mapping, dict):
        result = struct_collection.update_one(
            {'_id': company}, 
            {'$set': data},
            upsert=True
        )
        if result.acknowledged:
            return jsonify({'message': 'Document upserted'}), 200
    return jsonify({'error': 'Document is not a dict'}), 404


@structs.route('/mapping/<company>', methods=['GET'])
def read_mapping(company):
    """
    Read a single mapping from the collection by ID
    """
    document = struct_collection.find_one({'_id': company}, {'_id': 0})
    if document is None:
        return jsonify({'error': 'Document not found'}), 404
    else:
        return jsonify(document), 200


@structs.route('/mapping/<company>', methods=['DELETE'])
def delete_mapping(company):
    """
    Delete a single document from the collection by ID
    """
    result = struct_collection.delete_one({'_id': ObjectId(company)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Document not found'}), 404
    else:
        return jsonify({'message': 'Document deleted'}), 200
