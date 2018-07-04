from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run()