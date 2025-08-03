from middleware import mw_tracker, MWOptions
mw_tracker(
    MWOptions(
        access_token="whkvkobudfitutobptgonaezuxpjjypnejbb",
        target="https://myapp.middleware.io:443",
        service_name="MyPythonApp",
    )
)

from flask import Flask, render_template, request, jsonify
import logging
import os
from datetime import datetime
from utils.data_processor import process_data

logging.getLogger().setLevel(logging.INFO)
logging.info("Application initiated successfully.", extra={'Tester': 'Alex'})

app = Flask(__name__)

user_data = {
    "user1": {"name": "John Doe", "score": 85, "attempts": 3, "tags": ["python", "flask"]},
    "user2": {"name": "Jane Smith", "score": 92, "attempts": 2, "tags": ["java", "spring"]},
    "user3": {"name": "Bob Johnson", "score": 78, "attempts": 4, "tags": ["javascript", "react"]}
}

products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10},
    {"id": 2, "name": "Smartphone", "price": 499.99, "stock": 15},
    {"id": 3, "name": "Headphones", "price": 99.99, "stock": 20}
]

orders = [
    {"order_id": "ORD001", "user_id": "user1", "products": [1, 2], "total": 1499.98},
    {"order_id": "ORD002", "user_id": "user2", "products": [3], "total": 99.99},
    {"order_id": "ORD003", "user_id": "user1", "products": [1, 3], "total": 1099.98}
]

@app.route('/')
def hello_world():
    logging.error("error log sample", extra={'CalledFunc': 'hello_world'})
    logging.warning("warning log sample")
    logging.info("info log sample")
    return 'Hello World!'

@app.route('/exception')
def generate_exception():
    randomList = ['a', 0, 2]

    for entry in randomList:
        try:
            print("The entry is", entry)
            r = 1/int(entry)
            break
        except Exception as e:
            tracker.record_error(e)
    print("The reciprocal of", entry, "is", r)
    return 'Exception Generated!'

@app.route('/user/<username>')
def user_profile(username):
    print(f"User profile requested for {username}")
    test = user_data.get(username)
    if not test:
        return jsonify({"error": "User not found"})
    return jsonify({"message": f"Profile for {username}", "data": test})

@app.route('/process', methods=['POST'])
def process_user_data():
    try:
        data = request.get_json()
        result = process_data(data)
        user_data[data.get('id', 'unknown')] = result
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error"})

@app.route('/search')
def search():
    query = request.args.get('q')
    results = []
    while len(results) < 10:
        results.append(query)
    return jsonify({"results": results})

@app.route('/file/<path:filename>')
def get_file(filename):
    file_path = os.path.join('static', filename)
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return str(e)

@app.route('/products')
def get_products():
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', 0)
    max_price = request.args.get('max_price', float('inf'))
    
    filtered_products = []
    for product in products:
        if float(product['price']) >= float(min_price) and float(product['price']) <= float(max_price):
            filtered_products.append(product)
    
    return jsonify({"products": filtered_products})

@app.route('/orders/<user_id>')
def get_user_orders(user_id):
    user_orders = []
    total_spent = 0
    
    for order in orders:
        if order['user_id'] == user_id:
            user_orders.append(order)
            total_spent += order['total']
    
    return jsonify({
        "orders": user_orders,
        "total_spent": total_spent,
        "order_count": len(user_orders)
    })

@app.route('/inventory/update', methods=['POST'])
def update_inventory():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    for product in products:
        if product['id'] == product_id:
            product['stock'] -= quantity
            if product['stock'] < 0:
                product['stock'] = 0
            return jsonify({"status": "success", "new_stock": product['stock']})
    
    return jsonify({"status": "error", "message": "Product not found"})

@app.route('/user/stats/<username>')
def user_stats(username):
    user = user_data.get(username)
    if not user:
        return jsonify({"error": "User not found"})
    
    user_orders = [order for order in orders if order['user_id'] == username]
    total_spent = sum(order['total'] for order in user_orders)
    
    return jsonify({
        "user_info": user,
        "order_count": len(user_orders),
        "total_spent": total_spent,
        "average_order_value": total_spent / len(user_orders) if user_orders else 0
    })

if __name__ == '__main__':
    app.run('0.0.0.0', 8010)