from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['holding']
    format_collection = db['format']
    struct_collection = db['struct']
    data_collection = db['data']
except Exception as e:
    print('Cannot connect to DB ' + e)
    exit()


from src.format import format
from src.structs import structs
from src.data import data

app.register_blueprint(format)
app.register_blueprint(structs)
app.register_blueprint(data)

if __name__ == '__main__':
    app.run(debug=True)
