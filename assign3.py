# app.py
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS  # ✅ Добавляем CORS
from bson import ObjectId
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Разрешаем CORS для всех доменов

# MongoDB Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

if not app.config['MONGO_URI']:
    print("Ошибка: MONGO_URI не задан!")
    exit(1)

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Проверка соединения
if mongo.db is None:
    raise Exception("❌ Ошибка: Не удалось подключиться к MongoDB! Проверь MONGO_URI.")
else:
    print("✅ Успешное подключение к MongoDB!")

# Создание индексов
mongo.db.users.create_index("email", unique=True)
mongo.db.products.create_index("category")
mongo.db.orders.create_index("user_id")

# ✅ Главная страница
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the API'}), 200

# ✅ Добавление продукта
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    if not all(key in data for key in ['name', 'price', 'description', 'category', 'stock']):
        return jsonify({'error': 'Missing fields'}), 400
    data['_id'] = ObjectId()
    mongo.db.products.insert_one(data)
    return jsonify({'message': 'Product added successfully', 'product_id': str(data['_id'])}), 201

# ✅ Получение всех продуктов
@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(mongo.db.products.find({}, {'_id': 0}))
    return jsonify(products)

# ✅ Обновление продукта (PUT)
@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': data})
    return jsonify({'message': 'Product updated successfully'})

# ✅ Удаление продукта (DELETE)
@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    mongo.db.products.delete_one({'_id': ObjectId(product_id)})
    return jsonify({'message': 'Product deleted successfully'})

# ✅ Регистрация пользователя
@app.route('/api/users/register', methods=['POST'])
def register_user():
    data = request.json
    if not all(key in data for key in ['name', 'email', 'password', 'role']):
        return jsonify({'error': 'Missing fields'}), 400
    data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    data['_id'] = ObjectId()
    mongo.db.users.insert_one(data)
    return jsonify({'message': 'User registered successfully'}), 201

# ✅ Вход пользователя
@app.route('/api/users/login', methods=['POST'])
def login_user():
    data = request.json
    user = mongo.db.users.find_one({'email': data['email']})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity={'id': str(user['_id']), 'role': user['role']})
        return jsonify(access_token=access_token)
    return jsonify({'error': 'Invalid credentials'}), 401

# ✅ Создание заказа
@app.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.json
    user = get_jwt_identity()
    if not all(key in data for key in ['product_ids', 'order_status']):
        return jsonify({'error': 'Missing fields'}), 400
    order = {
        'user_id': ObjectId(user['id']),
        'product_ids': [ObjectId(pid) for pid in data['product_ids']],
        'order_status': data['order_status'],
        'timestamp': datetime.utcnow()
    }
    order['_id'] = ObjectId()
    mongo.db.orders.insert_one(order)
    return jsonify({'message': 'Order placed successfully', 'order_id': str(order['_id'])}), 201

# ✅ Получение заказов пользователя
@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user = get_jwt_identity()
    orders = list(mongo.db.orders.find({'user_id': ObjectId(user['id'])}, {'_id': 0}))
    return jsonify(orders)

# ✅ Обновление статуса заказа (PUT)
@app.route('/api/orders/<order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    data = request.json
    if 'order_status' not in data:
        return jsonify({'error': 'Missing order status'}), 400
    mongo.db.orders.update_one({'_id': ObjectId(order_id)}, {'$set': {'order_status': data['order_status']}})
    return jsonify({'message': 'Order status updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
