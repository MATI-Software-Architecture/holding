from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from app import data_collection, format_collection, struct_collection
from src import utils

data = Blueprint(
    'data_manager', __name__, url_prefix='/data'
)


@data.route('/<company>', methods=['POST'])
def create_document(company):
    """
    Create a new document in the collection
    """
    # check file exists
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if not file.filename.strip():
        return jsonify({'error': 'No selected file'}), 400

    ##############################
    # Orchestrator
    ##############################

    # get program and format
    format = file.filename.split('.')[-1]
    program = ''
    if format not in ['json', 'xml']:
        config = format_collection.find_one(
            {'format': format}, {'_id': 0, 'program': 1})
        if config is None:
            return jsonify({'error': 'No program found'}), 404
        program = config['program']

    # convert file
    content = file.stream.read().decode('utf-8')
    data = utils.convert(content, format, program)
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Invalid file or data'}), 400
    data = utils.flatten(data)

    ##############################
    # Validator
    ##############################

    # mapping fields
    mapping = struct_collection.find_one(
        {'_id': company}, {'_id': 0, 'mapping': 1}
    )
    if mapping:
        for key, value in mapping['mapping'].items():
            if value in data:
                data[key] = data.pop(value)

    # mandatory fields
    mandatory = struct_collection.find_one(
        {'_id': 'mandatory'}, {'_id': 0, 'fields': 1}
    )
    if mandatory:
        for field in mandatory['fields']:
            if field not in data:
                message = f'Missing mandatory field - {field}'
                return jsonify({'error': message}), 400

    # save file to database
    data['company'] = company
    result = data_collection.insert_one(data)
    return jsonify({'id': str(result.inserted_id)}), 201


@data.route('/', methods=['GET'])
def read_documents():
    """
    Read all documents from the collection
    """
    documents = []
    for document in data_collection.find():
        document['_id'] = str(document['_id'])
        documents.append(document)
    return jsonify(documents), 200


@data.route('/', methods=['DELETE'])
def delete_documents():
    """
    Delete all documents from the collection
    """
    result = data_collection.delete_many({})
    return jsonify({'count': result.deleted_count}), 200


@data.route('/<company>', methods=['GET'])
def read_document(company):
    """
    Read all documents from the collection
    """
    documents = []
    collection = data_collection.find({'company': company})
    for document in collection:
        document['_id'] = str(document['_id'])
        documents.append(document)
    return jsonify(documents), 200


@data.route('/<company>/<id>', methods=['DELETE'])
def delete_document(company, id):
    """
    Delete a single document from the collection by ID
    """
    result = data_collection.delete_one(
        {'_id': ObjectId(id), 'company': company})
    if result.deleted_count == 0:
        return jsonify({'error': 'Document not found'}), 404
    else:
        return jsonify({'id': id}), 200
