import json
from threading import Lock


class Order(object):

    def __init__(self):
        self.memory = []
        self.hasp_map = {}
        self.next_order = 1
        self.lock = Lock()

    def add_order(self, order):
        with self.lock:
            try:
                if not order['order_id'] in self.hasp_map:
                    self.memory.append(order)
                    self.hasp_map[order['order_id']] = len(self.memory) - 1
                    self.next_order += 1
                    return True
                else:
                    return False
            except Exception:
                return False

    def delete_order(self, order_id):
        with self.lock:
            try:
                if order_id in self.hasp_map:

                    # move the last order to the order to delete
                    index = self.hasp_map[order_id]
                    last_order = self.memory[-1]
                    self.memory[index] = last_order

                    # delete the last order
                    del self.memory[-1]

                    # update the hashtable
                    self.hasp_map[last_order['order_id']] = index
                    del self.hasp_map[order_id]

                    print(self.hasp_map)
                    return True
                else:
                    return False
            except Exception as e:
                print(f"error: {e}")
                return False

    def clean_up_memory(self):
        self.memory.clear()
        self.next_order = 1

    def get_memory(self):
        return self.memory

    def get_next_order(self):
        return self.next_order
