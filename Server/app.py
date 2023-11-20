from wpdb import WPDB
from flask import Flask, request, make_response
from flask_cors import CORS

myWPDB = WPDB()
app = Flask("wpdb")
CORS(app)
app.debug = True

@app.route('/insert', methods=['POST'])
def handle_insert():
    data = request.get_json()

    ret = myWPDB.insert_expenses(data)
    if ret:
        response_data = {'message': 'Success'}
        response = make_response(response_data, 200)
        response.headers['Content-Type'] = 'application/json'
    else:
        response_data = {'message': 'Failed'}
        response = make_response(response_data, 400)
        response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/delete', methods=['POST'])
def handle_delete():
    data = request.get_json()
    print(data)

    if "id" in data and data['id']: 
        id = data['id'] 
        print("id: ", id)
        ret = myWPDB.delete_expenses(id)  
    else:
        ret = False

    if ret:
        response_data = {'message': 'Success'}
        response = make_response(response_data, 200)
        response.headers['Content-Type'] = 'application/json'
    else:
        response_data = {'message': 'Failed'}
        response = make_response(response_data, 400)
        response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/get', methods=['POST'])
def handle_get():
    data = request.get_json()

    if "user_id" in data and data['user_id']: 
        id = data['user_id'] 
        print("id: ", id)
        ret = myWPDB.getProductData(id)  
    else:
        ret = False

    if ret:
        response_data = {'message': 'Success', 'query_data': ret}
        response = make_response(response_data, 200)
        response.headers['Content-Type'] = 'application/json'
        # print(f"1. {ret}\n")
        # print(f"2. {response_data}\n")
        # print(f"3. {response}\n")
    else:
        response_data = {'message': 'Failed'}
        response = make_response(response_data, 400)
        response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/update', methods=['POST'])
def handle_update():
    data = request.get_json()
    print(data)
    
    ret = myWPDB.updateProductData(data)
    if ret:
        response_data = {'message': 'Success'}
        response = make_response(response_data, 200)
        response.headers['Content-Type'] = 'application/json'
        print("response")
    else:
        response_data = {'message': 'Failed'}
        response = make_response(response_data, 400)
        response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/')
def hello():
    return "hello"

if __name__ == "__main__":
    
    app.run(debug=True, port=8080)
    myWPDB.close_db()
    print("db closed")