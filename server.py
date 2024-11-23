# server.py

from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
import hashlib

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.erp_database

# Hash function for password security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Example: Predefined admin users with hashed passwords
db.admins.insert_one({'username': 'admin', 'password': hash_password('admin123')})

# Middleware for admin authentication
def authenticate_admin(username, password):
    admin = db.admins.find_one({'username': username, 'password': hash_password(password)})
    if not admin:
        abort(401, description="Unauthorized: Invalid credentials")

@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        abort(400, description="Missing username or password")
    
    # Authenticate the admin
    authenticate_admin(username, password)
    return jsonify({'message': 'Login successful, access granted to admin.'})

# Add a new record (admin only)
@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    authenticate_admin(data.get('username'), data.get('password'))
    
    item = {
        'name': data.get('name'),
        'category': data.get('category'),
        'quantity': int(data.get('quantity'))
    }
    db.items.insert_one(item)
    return jsonify({'message': 'Record added successfully'})

# View all records (open to everyone)
@app.route('/view_records', methods=['GET'])
def view_records():
    items = list(db.items.find({}, {'_id': 0}))
    return jsonify(items)

# Update item quantity (admin only)
@app.route('/update_record', methods=['PUT'])
def update_record():
    data = request.json
    authenticate_admin(data.get('username'), data.get('password'))
    
    query = {'name': data.get('name')}
    new_quantity = int(data.get('quantity'))
    
    # Update quantity
    result = db.items.update_one(query, {'$set': {'quantity': new_quantity}})
    if result.matched_count == 0:
        abort(404, description="Item not found")

    # Send acknowledgment if deficit
    if new_quantity <= 0:
        return jsonify({'message': 'Quantity updated. Acknowledgment: Item is in deficit!'})
    return jsonify({'message': 'Quantity updated successfully'})

# Delete an item (admin only)
@app.route('/delete_record', methods=['DELETE'])
def delete_record():
    data = request.json
    authenticate_admin(data.get('username'), data.get('password'))
    
    query = {'name': data.get('name')}
    result = db.items.delete_one(query)
    if result.deleted_count == 0:
        abort(404, description="Item not found")
    return jsonify({'message': 'Record deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
