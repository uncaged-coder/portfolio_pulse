from typing import List, Dict
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource
from portfolio_pulse.data_source_csv import DataSourceCSV
from portfolio_pulse.data_source_woob import DataSourceWoob


# AccountManager to handle multiple accounts with different data sources
class AccountManager:
    def __init__(self, account_config: Dict):
        """
        account_config: Dictionary of account_name and data source type.
        Example:
        {
            "Account1": {"type": "csv", "file_path": "path/to/file.csv"},
            "Account2": {"type": "woob"},
            ...
        }
        """
        self.accounts = {}
        for account_name, config in account_config.items():
            data_source = self.create_data_source(config)
            self.accounts[account_name] = data_source

    def create_data_source(self, config: Dict) -> DataSource:
        """Factory method to create the appropriate data source based on config."""
        source_type = config.get("type")
        if source_type == "csv":
            return DataSourceCSV(config["file_path"])
        elif source_type == "woob":
            return DataSourceWoob()
        else:
            raise ValueError(f"Unsupported data source type: {source_type}")

    def fetch_all_assets(self) -> Dict[str, List[Asset]]:
        """Fetches assets from all accounts."""
        all_assets = {}
        for account_name, data_source in self.accounts.items():
            all_assets[account_name] = data_source.fetch_assets()
        return all_assets
