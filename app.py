from flask import Flask
from src.format import format
from src.structs import structs
from src.data import data

app = Flask(__name__)

app.register_blueprint(format)
app.register_blueprint(structs)
app.register_blueprint(data)

if __name__ == '__main__':
    app.run(debug=True)
