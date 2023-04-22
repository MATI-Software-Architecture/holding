from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['holding']
config_collection = db['config']
core_collection = db['core']


from src.config import config
from src.core import core

app.register_blueprint(config)
app.register_blueprint(core)

if __name__ == '__main__':
    app.run(debug=True)
