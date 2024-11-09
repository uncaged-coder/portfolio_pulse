
class Asset:
    def __init__(self, name: str, broker: str, isin: str, category: str, quantity: float, price: float):
        self.name = name
        self.isin = isin
        self.category = category
        self.quantity = quantity
        self.price = price
        self.broker = broker

    def value(self) -> float:
        """Calculate the value of the asset based on price and quantity."""
        return self.price * self.quantity

