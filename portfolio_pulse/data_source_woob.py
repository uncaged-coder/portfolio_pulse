import subprocess
from typing import List
from woob.core import Woob
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource
from portfolio_pulse.broker_handler_woob import BrokerHandlerWoob
from portfolio_pulse.broker_handler_aucoffre import BrokerHandlerAucoffre
from portfolio_pulse.broker_handler_bullionstar import BrokerHandlerBullionstar
from portfolio_pulse.broker_handler_degiro import BrokerHandlerDegiro


class DataSourceWoob(DataSource):
    def __init__(self, broker_config_section):
        self.brokername = broker_config_section.name
        self.handler = self._initialize_handler()
        self.woob = self._initialize_woob(broker_config_section)

    def _fetch_credentials(self, broker_section) -> dict:
        """Fetch login and password based on broker configuration."""
        return self.handler.get_login_data(broker_section)

    def _initialize_woob(self, broker_section) -> Woob:
        """Initialize Woob and load backend based on broker config."""
        woob = Woob()
        credentials = self._fetch_credentials(broker_section)
        woob.load_backend(self.brokername, self.brokername, credentials)
        return woob

    def _initialize_handler(self):
        """Initialize broker-specific handler."""
        if self.brokername == "aucoffre":
            return BrokerHandlerAucoffre(self.brokername)
        elif self.brokername == "bullionstar":
            return BrokerHandlerBullionstar(self.brokername)
        elif self.brokername == "degiro":
            return BrokerHandlerDegiro(self.brokername)
        return BrokerHandlerWoob(self.brokername)

    def fetch_assets(self) -> List[Asset]:
        """Fetch assets for the broker using the handler."""
        assets = []
        print(f"====== {self.brokername} =======")
        broker = self.woob.get_backend(self.brokername)

        for account in self.woob.iter_accounts():
            for investment in broker.iter_investment(account):
                asset = self.handler.process_investment(investment)
                assets.append(asset)

        return assets
