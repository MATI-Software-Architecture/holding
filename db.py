from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['holding']

format_collection = db['format']
struct_collection = db['struct']
data_collection = db['data']
