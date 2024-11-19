from flask import Flask, jsonify, request
from flask_login import login_user, current_user, logout_user, login_required
from database import db
from login_manager import login_manager
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return jsonify({'message': 'Authenticated successfully'})
    return jsonify({'message': 'Invalid credentials'}), 400

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successfully'})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User(username = username, password = password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User successfully registered'})
    
    return jsonify({'message': 'Invalid data'}), 400

@app.route('/user/<int:id_user>', methods = ['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    if user:
        return jsonify({'username': f'{user.username}'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:id_user>', methods = ['PUT'])
@login_required
def update_user(id_user):
    user = User.query.get(id_user)
    if user:
        data = request.json
        user.password = data.get('password')
        db.session.commit()
        return jsonify({'message': f'{user.username} updated successfully'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delte_user(id_user):
    user = User.query.get(id_user)
    if user.id == current_user.id:
        return jsonify({'message': 'Unauthorized deletion'}), 403
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'{user.username} deleted successfully'})
    return jsonify({'message': 'User not found'}), 404
if __name__ == '__main__':
    app.run(debug=True, port=8000)