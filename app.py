from flask import Flask, request, json, Response
from pymongo import MongoClient
from pyparsing import col
import dns
import json

#Creating class for mongodb atlas connectivity
class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb+srv://Gaurav27:gaurav@cluster0.h0kk1.gcp.mongodb.net/rms?retryWrites=true&w=majority")
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def add(self, data):
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def modify(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output     


# Creating the flask app
app = Flask(__name__)

#################################################################
# TEST API ENDPOINTS
#################################################################

# defining a route
@app.route("/")
def home():
    # returning a response
    return Response(response=json.dumps({"System Status": "Api System Working Fine!!"}),
                    status=200,
                    mimetype='application/json')


#################################################################
# MENU API ENDPOINTS
#################################################################

#To view the menu
@app.route('/menu', methods=['GET'])
def menu_read():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

#To add the item to menu
@app.route('/menu', methods=['POST'])
def menu_write():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.add(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json') 

#To modify the menu item
@app.route('/menu', methods=['PUT'])
def menu_update():
    data = request.json
    if data is None or data == {} or 'DataToBeUpdated' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.modify()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

#To delete the menu item
@app.route('/menu', methods=['DELETE'])
def menu_delete():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.delete(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json') 



#################################################################
# Order API ENDPOINTS
#################################################################
#To view the order
@app.route('/order', methods=['GET'])
def order_read():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

#To create the order
@app.route('/order', methods=['POST'])
def order_write():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.add(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json') 

#To modify the order item
@app.route('/order', methods=['PUT'])
def order_update():
    data = request.json
    if data is None or data == {} or 'DataToBeUpdated' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.modify()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

#To delete the order
@app.route('/order', methods=['DELETE'])
def order_delete():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.delete(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')                     

#Main function to start the flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')