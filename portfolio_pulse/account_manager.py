import configparser
import os
from typing import List, Dict
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource
from portfolio_pulse.data_source_csv import DataSourceCSV
from portfolio_pulse.data_source_woob import DataSourceWoob
from portfolio_pulse.data_source_ccxt import DataSourceCcxt
from portfolio_pulse.data_source_ibkr import DataSourceIBKR


class AccountManager:
    def __init__(self, user: str):
        self.user = user
        config_path = os.path.expanduser(f"~/.config/portfolio_pulse/{user}.ini")
        self.config = self._load_config(config_path)

        # Mapping of supported data source types to their respective classes
        self.data_sources = {
            "csv": DataSourceCSV,
            "woob": DataSourceWoob,
            "ccxt": DataSourceCcxt,
            "ibkr": DataSourceIBKR
        }

    def _load_config(self, config_path: str) -> configparser.ConfigParser:
        """Load configuration file for multiple brokers."""
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def create_data_source(self, source_type: str, config_section: configparser.SectionProxy) -> DataSource:
        """Factory method to create the appropriate data source based on config."""
        data_source_class = self.data_sources.get(source_type)
        if not data_source_class:
            raise ValueError(f"Unsupported data source type: {source_type}")
        return data_source_class(config_section)

    def fetch_all_assets(self) -> Dict[str, List[Asset]]:
        all_assets = {}

        for account_name in self.config.sections():
            #broker_name = self.config["broker"] if "broker" in self.config else account_name
            config_section = self.config[account_name]
            source_type = config_section.get("type")

            if source_type not in self.data_sources:
                print(f"Warning: Unsupported source type '{source_type}' in section '{account_name}'")
                continue

            # Create the data source and fetch assets
            data_source = self.create_data_source(source_type, config_section)
            all_assets[account_name] = data_source.fetch_assets()

        return all_assets
