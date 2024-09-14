import datetime
import json

from flask import Flask, request, abort
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS

from Models.Order import Order
from Models.SocketIOModel import SocketIOModel

## initalize the app
app = Flask(__name__)
socketio = SocketIO(app)
order = Order()
model = SocketIOModel('/cafe-8-backend', order, socketio)
model.set_order(order)
socketio.on_namespace(model)
CORS(app)

## Tag Add price, is it necessary to make client and Tablet isolate?

# # Middleware to block all requests except /client and /server namespaces
@app.before_request
def block_non_socketio_requests():
    if request.path not in ['/socket.io/', '/getOrderNumber', '/getMenu', '/getTags', '/getTables', '/getOrder']:
        abort(403)  # Forbidden


@app.route('/getOrderNumber', methods=['GET'])
def generate_order_number():
    current_date = datetime.datetime.now()
    return [int(current_date.strftime("%y%m%d%H%M%S") + f"{order.get_next_order()%1000:03}")]


@app.route('/getMenu', methods=['GET'])
def get_menu():
    file = open("./Config/Menu.json", 'r')
    menu = json.load(file)
    file.close()
    return menu


@app.route('/getTags', methods=['GET'])
def get_tags():
    file = open("./Config/Tags.json")
    tags = json.load(file)
    file.close()
    return tags


@app.route('/getTables', methods=['GET'])
def get_tables():
    file = open("./Config/Table.json")
    tags = json.load(file)
    file.close()
    return tags


@app.route('/getOrder', methods=['GET'])
def get_order():
    return order.get_memory()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
