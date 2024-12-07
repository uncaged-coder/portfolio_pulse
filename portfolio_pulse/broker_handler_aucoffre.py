import subprocess
from portfolio_pulse.asset import Asset
from portfolio_pulse.broker_handler_woob import BrokerHandlerWoob


class BrokerHandlerAucoffre(BrokerHandlerWoob):

    def get_login_data(self, broker_section):
        pseudo = broker_section.get('pseudo')
        password_entry = broker_section.get('password_entry')

        if not pseudo or not password_entry:
            raise ValueError("Missing pseudo or password entry in broker configuration.")

        pass_data = subprocess.check_output(['pass', password_entry]).decode().strip().split('\n')
        identifiant = pass_data[0]
        secret = pass_data[1]
        return {'pseudo': pseudo, 'identifiant': identifiant, 'secret': secret}

    def process_investment(self, investment) -> Asset:
        """Processes investment data and assigns the appropriate category and values."""

        asset = super().process_investment(investment)
        if asset.category == "Stocks":
            asset.category = "Gold"
        return asset
