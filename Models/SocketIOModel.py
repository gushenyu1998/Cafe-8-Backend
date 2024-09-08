import json

from flask import Flask, jsonify, request
from flask_socketio import emit, SocketIO, Namespace
from Models.Order import Order


class SocketIOModel(Namespace):
    order = None
    socketio = None
    def __init__(self, namespace, order, socketio):
        super().__init__(namespace)
        self.order = order
        self.socketio = socketio

    def set_order(self, order):
        self.order = order

    def on_connect(self):
        emit('message', f"id:{request.sid} Connect Success")

    def on_disconnect(self):
        emit('message', f"{request.sid} disconnected from {self.namespace}")

    def on_error(self, error):
        emit('message', f"{request.sid} meets error {error}")

    def on_addOrder(self, one_order):
        if self.order:
            try:
                if one_order['order_id']:
                    if self.order.add_order(one_order):
                        emit('message', f"Success: Update the Order", broadcast=True)
                        return "Success"
                    else:
                        emit('message', f"Error: System busy, please retry")
                        return "Fail"
                else:
                    emit('message', f"Error: order not fit for the format")
                    return "Fail"
            except Exception as e:
                emit('message', f"Error: order not a JSON object: {e}")
                return "Fail"
        else:
            emit('message', f"Error: order append due to the data error in backend")
            return "Fail"

    def on_removeOrder(self, order_id):
        if self.order:
            try:
                if order_id['order_id']:
                    if self.order.delete_order(order_id['order_id']):
                        emit('message', f"Success: Update the Order", broadcast=True)
                        return "Success"
                    else:
                        emit('message', f"Error: order id not found")
                        return "Fail"
                emit('message', f"Error: order not fit for the format")
                return "Fail"
            except Exception as e:
                emit('message', f"Error: order not a JSON object: {e}")
                return "Fail"
        else:
            emit('message', f"Error: order append due to the data error in backend")
            return "Fail"

    # def on_message(self, data):
    #     emit('message', data, broadcast=True)
