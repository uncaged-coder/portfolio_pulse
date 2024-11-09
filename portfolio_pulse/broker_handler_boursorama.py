from portfolio_pulse.asset import Asset
from portfolio_pulse.broker_handler import BrokerHandler


class BrokerHandlerBoursorama(BrokerHandler):
    """Handler for Boursorama-specific asset adjustments."""

    def process_investment(self, investment) -> Asset:
        """Adjusts Boursorama assets based on custom rules."""

        name = investment.label
        isin = investment.code
        if isin == "XX-liquidity":
            category = "Currencies"
            unit_price = 1
            quantity = investment.valuation
        else:
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
