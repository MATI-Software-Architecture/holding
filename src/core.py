from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from app import core_collection, config_collection
from src.utils import convert

core = Blueprint(
    'core_manager', __name__, url_prefix='/core', template_folder='templates'
)

@core.route('/', methods=['POST'])
def create_document():
    """
    Create a new document in the collection
    """
    # check headers
    headers = request.headers
    org_id = headers.get('x-hx-orgid')
    if not org_id:
        return jsonify({'error': 'Missing headers'}), 400

    # check file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if not file.filename.strip():
        return jsonify({'error': 'No selected file'}), 400

    # convert file from any format to json
    format = file.filename.split('.')[-1]
    config = config_collection.find_one({'format': format}, {'_id': 0, 'program': 1})
    if config is None:
        return jsonify({'error': 'No program found'}), 404
    content = file.stream.read().decode('utf-8')
    data = convert(content, format, config['program'])

    # save file to database
    result = core_collection.insert_one(data)
    return jsonify({'id': str(result.inserted_id)}), 201


@core.route('/', methods=['GET'])
def read_documents():
    """
    Read all documents from the collection
    """
    documents = []
    for document in core_collection.find():
        document['_id'] = str(document['_id'])
        documents.append(document)
    return jsonify(documents), 200