from Flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello-world', methods=['GET'])
def hello_world():
    return jsonify({'message': 'hello world'})

if __name__ == '__main__':
    app.run(debug=True)