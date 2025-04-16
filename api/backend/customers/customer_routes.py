########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
customers = Blueprint('customers', __name__)


#------------------------------------------------------------
# Get all customers from the system
@customers.route('/customers', methods=['GET'])
def get_customers():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT id, company, last_name,
                    first_name, job_title, business_phone FROM customers
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update customer info for customer with particular userID
#   Notice the manner of constructing the query.
@customers.route('/customers', methods=['PUT'])
def update_customer():
    current_app.logger.info('PUT /customers route')
    cust_info = request.json
    cust_id = cust_info['id']
    first = cust_info['first_name']
    last = cust_info['last_name']
    company = cust_info['company']

    query = 'UPDATE customers SET first_name = %s, last_name = %s, company = %s where id = %s'
    data = (first, last, company, cust_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'customer updated!'

#------------------------------------------------------------
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    current_app.logger.info('GET /customers/<userID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT id, first_name, last_name FROM customers WHERE id = {0}'.format(userID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Makes use of the very simple ML model in to predict a value
# and returns it to the user
@customers.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


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
    
    # Get the ID of the newly created customer
    cursor.execute('SELECT LAST_INSERT_ID()')
    new_id = cursor.fetchone()[0]
    
    return make_response(jsonify({'id': new_id, 'message': 'Customer created'}), 201)

#------------------------------------------------------------
# Create a new customer in the system
#   Notice the parameterized query for security
@customers.route('/customers', methods=['POST'])
def add_customer():
    current_app.logger.info('POST /customers route')
    cust_info = request.json
    
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
    return 'customer added!'

#------------------------------------------------------------
# Delete a customer with particular userID from the system
#   First checks if customer exists before attempting deletion
@customers.route('/customers/<userID>', methods=['DELETE'])
def delete_customer(userID):
    current_app.logger.info(f'DELETE /customers/{userID} route')
    
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM customers WHERE id = %s', (userID,))
    db.get_db().commit()
    return 'customer deleted!'

#------------------------------------------------------------
# Search customers by name or company using query parameter
#   Uses LIKE with wildcards for flexible searching
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
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get detailed customer information including order statistics
#   Joins with orders table to provide comprehensive view
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
    
    theData = cursor.fetchone()
    columns = [col[0] for col in cursor.description]
    result = dict(zip(columns, theData)) if theData else {}
    
    the_response = make_response(jsonify(result))
    the_response.status_code = 200 if theData else 404
    return the_response

#------------------------------------------------------------
# Perform bulk customer operations (create/update/delete)
#   Accepts array of operations to process in single transaction
@customers.route('/customers/bulk', methods=['POST'])
def bulk_operations():
    current_app.logger.info('POST /customers/bulk route')
    
    operations = request.json
    cursor = db.get_db().cursor()
    results = []
    
    for op in operations:
        try:
            if op['action'] == 'create':
                # Implementation similar to single create
                pass
            elif op['action'] == 'update':
                # Implementation similar to single update
                pass
            # Add other actions as needed
        except Exception as e:
            results.append({'error': str(e)})
    
    db.get_db().commit()
    the_response = make_response(jsonify(results))
    the_response.status_code = 207
    return the_response