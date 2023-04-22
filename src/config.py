from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from app import config_collection
from src import utils

config = Blueprint(
    'config_manager', __name__, url_prefix='/config', template_folder='templates'
)

@config.route('/', methods=['POST'])
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
    result = config_collection.insert_one(data)
    return jsonify({'id': str(result.inserted_id)}), 201


@config.route('/', methods=['GET'])
def read_documents():
    """
    Read all documents from the collection
    """
    documents = []
    for document in config_collection.find():
        document['_id'] = str(document['_id'])
        documents.append(document)
    return jsonify(documents), 200


@config.route('/<id>', methods=['GET'])
def read_document(id):
    """
    Read a single document from the collection by ID
    """
    document = config_collection.find_one({'_id': ObjectId(id)})
    if document is None:
        return jsonify({'error': 'Document not found'}), 404
    else:
        document['_id'] = str(document['_id'])
        return jsonify(document), 200


@config.route('/<id>', methods=['PUT'])
def update_document(id):
    """
    Update a single document in the collection by ID
    """
    data = request.json
    result = config_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count == 0:
        return jsonify({'error': 'Document not found'}), 404
    else:
        return jsonify({'message': 'Document updated'}), 200


@config.route('/<id>', methods=['DELETE'])
def delete_document(id):
    """
    Delete a single document from the collection by ID
    """
    result = config_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Document not found'}), 404
    else:
        return jsonify({'message': 'Document deleted'}), 200
