from portfolio_pulse.asset import Asset
from portfolio_pulse.broker_handler import BrokerHandler


class BrokerHandlerGeneric(BrokerHandler):
    """Default handler for brokers with no specific adjustments."""

    def process_investment(self, investment) -> Asset:
        """Processes investments without any special adjustments."""

        name = investment.label
        isin = investment.code
        category = "Stocks"  # Default category
        unit_price = investment.unitprice
        quantity = investment.quantity

        return Asset(
            name=name,
            isin=isin,
            category=category,
            quantity=quantity,
            price=unit_price
        )
