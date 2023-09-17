class OrderBook:
    def __init__(self) -> None:
        self.buys = []
        self.sells = []
        self.id = 0
        self.all_orders = {}

    def insert_order(self, order):
        order_id = self.id
        order['id'] = order_id
        if order['side'].lower() == 'b':
            self.buys.append(order)
        elif order['side'].lower() == 's':
            self.sells.append(order)
        self.all_orders[order_id] = order
        self.id += 1
        return order_id

    def modify_order(self, order: dict):
        order_id = order.get('id', None)
        if order_id is None:
            raise KeyError("No id found.")
        if order['side'].lower() not in ['b','s']:
            raise ValueError("Invalid side")
            
        
        
        old_order_side = self.all_orders[order_id]['side'].lower()
        new_order_side = order['side'].lower()
        for key, value in order.items():
            self.all_orders[order_id][key] = value


        if old_order_side != new_order_side:
            if old_order_side == 'b':
                for i, buy_order in enumerate(self.buys):
                    if buy_order['id'] == order_id:
                        self.sells.append(self.buys.pop(i))
            elif old_order_side == 's':
                for i, sell_order in enumerate(self.sells):
                    if sell_order['id'] == order_id:
                        self.buys.append(self.sells.pop(i))
        
        return order_id

    def delete_order(self, order_id: int):
        is_valid_order_id = order_id in self.all_orders
        if is_valid_order_id:
            keys = self.all_orders[order_id].keys()
            for key in keys:
                self.all_orders[order_id].pop(key)
                print(self.all_orders)
                print(self.sells)
        return is_valid_order_id
        
        
        

ob1 = OrderBook()
o1 = {'price': 10, 'quantity': 100, 'side':'B'}
o2 = {'price': 11, 'quantity': 50, 'side':'B'}
o3 = {'price': 9, 'quantity': 70, 'side':'B'}
print(ob1.insert_order(o1))
# print(ob1.insert_order(o2))
# print(ob1.insert_order(o3))
print("BEFORE MODIFY ORDER")
print(f"Buys: {ob1.buys}")
print(f"Sells: {ob1.sells}")
print(ob1.all_orders)
o4 = {'id':0, 'price':11000000, 'quantity':100, 'side':'S'}
ob1.modify_order(o4)
print("AFTER MODIFY ORDER")
print(f"Buys: {ob1.buys}")
print(f"Sells: {ob1.sells}")
ob1.delete_order(0)
# print(ob1.sells)
print(ob1.all_orders)