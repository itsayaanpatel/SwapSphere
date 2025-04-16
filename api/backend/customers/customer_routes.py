from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Create the blueprint
customers = Blueprint('customers', __name__)

# ------------------------------------------------------------
# Get all customers
@customers.route('/customers', methods=['GET'])
def get_customers():
    current_app.logger.info('GET /customers route')
    
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT id, company, last_name,
                    first_name, job_title, business_phone FROM customers''')
    
    theData = cursor.fetchall()
    return make_response(jsonify(theData), 200)

# ------------------------------------------------------------
# Get specific customer
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    current_app.logger.info(f'GET /customers/{userID} route')
    
    cursor = db.get_db().cursor()
    cursor.execute('SELECT id, first_name, last_name FROM customers WHERE id = %s', (userID,))
    
    theData = cursor.fetchall()
    return make_response(jsonify(theData), 200)

# ------------------------------------------------------------
# Create new customer
@customers.route('/customers', methods=['POST'])
def add_customer():
    current_app.logger.info('POST /customers route')
    cust_info = request.json
    
    # Validate required fields
    if not all(key in cust_info for key in ['first_name', 'last_name', 'company']):
        return make_response(jsonify({'error': 'Missing required fields'}), 400)
    
    query = '''INSERT INTO customers 
               (first_name, last_name, company, job_title, business_phone) 
               VALUES (%s, %s, %s, %s, %s)'''
    data = (
        cust_info['first_name'],
        cust_info['last_name'],
        cust_info['company'],
        cust_info.get('job_title', ''),
        cust_info.get('business_phone', '')
    )
    
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    
    # Return the ID of the newly created customer
    cursor.execute('SELECT LAST_INSERT_ID()')
    new_id = cursor.fetchone()[0]
    return make_response(jsonify({'id': new_id, 'message': 'Customer created'}), 201)

# ------------------------------------------------------------
# Update customer
@customers.route('/customers', methods=['PUT'])
def update_customer():
    current_app.logger.info('PUT /customers route')
    cust_info = request.json
    
    query = 'UPDATE customers SET first_name = %s, last_name = %s, company = %s WHERE id = %s'
    data = (
        cust_info['first_name'],
        cust_info['last_name'],
        cust_info['company'],
        cust_info['id']
    )
    
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return make_response(jsonify({'message': 'Customer updated'}), 200)

# ------------------------------------------------------------
# Delete customer
@customers.route('/customers/<userID>', methods=['DELETE'])
def delete_customer(userID):
    current_app.logger.info(f'DELETE /customers/{userID} route')
    
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM customers WHERE id = %s', (userID,))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Customer deleted'}), 200)

# ------------------------------------------------------------
# Search customers
@customers.route('/customers/search', methods=['GET'])
def search_customers():
    current_app.logger.info('GET /customers/search route')
    
    search_term = request.args.get('q', '')
    query = '''SELECT id, company, last_name, first_name 
               FROM customers 
               WHERE first_name LIKE %s OR last_name LIKE %s OR company LIKE %s'''
    search_pattern = f'%{search_term}%'
    
    cursor = db.get_db().cursor()
    cursor.execute(query, (search_pattern, search_pattern, search_pattern))
    theData = cursor.fetchall()
    return make_response(jsonify(theData), 200)

# ------------------------------------------------------------
# Get customer details with stats
@customers.route('/customers/<userID>/details', methods=['GET'])
def get_customer_details(userID):
    current_app.logger.info(f'GET /customers/{userID}/details route')
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT c.*, 
               COUNT(o.id) as order_count,
               SUM(o.total) as total_spent
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        WHERE c.id = %s
        GROUP BY c.id
    ''', (userID,))
    
    result = cursor.fetchone()
    if not result:
        return make_response(jsonify({'error': 'Customer not found'}), 404)
    
    columns = [col[0] for col in cursor.description]
    return make_response(jsonify(dict(zip(columns, result))), 200)

# ------------------------------------------------------------
# ML Prediction endpoint
@customers.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'GET /prediction/{var01}/{var02} route')
    
    returnVal = predict(var01, var02)
    return make_response(jsonify({'result': returnVal}), 200)