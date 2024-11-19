from flask import Flask, jsonify
from database import db
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/hello-world', methods=['GET'])
def hello_world():
    return jsonify({'message': 'hello world'})

if __name__ == '__main__':
    app.run(debug=True)