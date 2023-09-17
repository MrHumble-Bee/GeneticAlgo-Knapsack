class Order:
    def __init__(self, price, quantity, side) -> None:
        self.price = price
        self.quantity = quantity
        self.side = side

    def verify_negativity(self):
        if not isinstance(self.quantity, int):
            print("The current quantity is not an integer.")
            return

        if self.quantity < 0:
            print("Negative quantity.")
        else:
            print("Positive quantity.")
        return