import json
from flask import Flask, jsonify, request, abort
import MySQLdb

app = Flask(__name__)

# Load database credentials from a JSON file
with open('config_file.json') as config_file:
    config = json.load(config_file)

# Connect to the database
db = MySQLdb.connect(
    host=config['host'],
    user=config['user'],
    passwd=config['passwd']
)

# Use a cursor to interact with the database
cursor = db.cursor()
print(cursor.execute("show databases;"))
# Routes for CRUD operations

@app.route('/items', methods=['GET'])
def get_items():
    """Retrieve all items"""
    cursor.execute("SELECT * FROM items;")
    items = cursor.fetchall()
    # Convert to a list of dictionaries
    items_list = [{"id": row[0], "name": row[1], "description": row[2]} for row in items]
    return jsonify(items_list)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve a specific item by ID"""
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if not item:
        abort(404)  # Not Found
    item_dict = {"id": item[0], "name": item[1], "description": item[2]}
    return jsonify(item_dict)

@app.route('/items', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.json
    if 'name' not in data or 'description' not in data:
        abort(400)  # Bad Request

    cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (data['name'], data['description']))
    db.commit()
    new_id = cursor.lastrowid
    data['id'] = new_id
    return jsonify(data), 201  # Created

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    data = request.json
    if 'name' not in data or 'description' not in data:
        abort(400)  # Bad Request

    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if not item:
        abort(404)  # Not Found

    cursor.execute("UPDATE items SET name = %s, description = %s WHERE id = %s", (data['name'], data['description'], item_id))
    db.commit()
    data['id'] = item_id
    return jsonify(data)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if not item:
        abort(404)  # Not Found

    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    db.commit()
    return '', 204  # No Content

# Run the application
if __name__ == '__main__':
    app.run(debug=True)