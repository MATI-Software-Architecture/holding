from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from app import format_collection
from src import utils

format = Blueprint(
    'format_manager', __name__, url_prefix='/config/format'
)

@format.route('/', methods=['POST'])
def create_document():
    """
    Create a new document in the collection
    """
    data = request.json
    package = data.get('package')
    if package:
        try:
            utils.install(package)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    result = format_collection.insert_one(data)
    return jsonify({'id': str(result.inserted_id)}), 201


@format.route('/', methods=['GET'])
def read_documents():
    """
    Read all documents from the collection
    """
    documents = []
    for document in format_collection.find():
        document['_id'] = str(document['_id'])
        documents.append(document)
    return jsonify(documents), 200


@format.route('/<id>', methods=['GET'])
def read_document(id):
    """
    Read a single document from the collection by ID
    """
    document = format_collection.find_one({'_id': ObjectId(id)})
    if document is None:
        return jsonify({'error': 'Document not found'}), 404
    else:
        document['_id'] = str(document['_id'])
        return jsonify(document), 200


@format.route('/<id>', methods=['PUT'])
def update_document(id):
    """
    Update a single document in the collection by ID
    """
    data = request.json
    result = format_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count == 0:
        return jsonify({'error': 'Document not found'}), 404
    else:
        return jsonify({'message': 'Document updated'}), 200


@format.route('/<id>', methods=['DELETE'])
def delete_document(id):
    """
    Delete a single document from the collection by ID
    """
    result = format_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Document not found'}), 404
    else:
        return jsonify({'message': 'Document deleted'}), 200
