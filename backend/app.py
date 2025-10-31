from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Mzanzibari Backend API"})

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"status": "ok", "info": "Sample Flask endpoint"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
