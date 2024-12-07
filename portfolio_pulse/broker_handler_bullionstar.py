import subprocess
from portfolio_pulse.asset import Asset
from portfolio_pulse.broker_handler_woob import BrokerHandlerWoob


class BrokerHandlerBullionstar(BrokerHandlerWoob):

    def process_investment(self, investment) -> Asset:
        """Processes investment data and assigns the appropriate category and values."""

        asset = super().process_investment(investment)
        if asset.category == "Stocks":
            asset.category = "Gold"
        return asset
