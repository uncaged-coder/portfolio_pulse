import os
import configparser
import subprocess
from typing import List
from woob.core import Woob
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource
from portfolio_pulse.broker_handler_boursorama import BrokerHandlerBoursorama
from portfolio_pulse.broker_handler_generic import BrokerHandlerGeneric


class DataSourceWoob(DataSource):
    def __init__(self, config_path: str = "~/.config/portfolio_pulse/config.ini"):
        self.config = self._load_config(config_path)
        self.woob = self._initialize_woob()
        self.handlers = self._initialize_handlers()

    def _load_config(self, config_path: str) -> configparser.ConfigParser:
        """Load configuration file for multiple brokers."""
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(config_path))
        return config

    def _fetch_credentials(self, broker_section: configparser.SectionProxy) -> dict:
        """Fetch login and password using pass based on broker configuration."""
        login = broker_section.get('login')
        password_entry = broker_section.get('password_entry')

        if not login or not password_entry:
            raise ValueError("Missing login or password entry in broker configuration.")

        password = subprocess.check_output(['pass', password_entry]).decode().strip().split('\n')[0]
        return {'login': login, 'password': password}

    def _initialize_woob(self) -> Woob:
        """Initialize Woob and load each broker backend based on the config."""
        woob = Woob()

        for broker_name, broker_config in self.config.items():
            if broker_config.get('type') == 'woob':
                credentials = self._fetch_credentials(broker_config)
                woob.load_backend(broker_name, broker_name, credentials)

        return woob

    def _initialize_handlers(self) -> dict:
        """Initialize broker-specific handlers."""
        handlers = {}

        for broker_name in self.config.sections():
            if broker_name == "boursorama":
                handlers[broker_name] = BrokerHandlerBoursorama(broker_name)
            else:
                handlers[broker_name] = BrokerHandlerGeneric(broker_name)

        return handlers

    def fetch_assets(self) -> List[Asset]:
        """Fetch assets for each configured Woob broker, applying specific broker rules."""
        assets = []

        for broker_name, broker_config in self.config.items():
            if broker_config.get('type') != 'woob':
                continue

            broker = self.woob.get_backend(broker_name)
            handler = self.handlers.get(broker_name, BrokerHandlerGeneric(broker_name))

            for account in broker.iter_accounts():
                for investment in broker.iter_investment(account):
                    asset = handler.process_investment(investment)
                    assets.append(asset)

        return assets
