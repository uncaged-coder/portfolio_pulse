from typing import List
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource


class DataSourceCSV(DataSource):
    def __init__(self, user: str):
        super.__init__(self, user)

    def fetch_assets(self, file_path) -> List[Asset]:
        assets = []
        with open(file_path, "r") as file:
            for line in file.readlines()[1:]:  # Skip header
                name, isin, category, quantity, price = line.strip().split(',')
                assets.append(Asset(name, isin, category, float(quantity), float(price)))
        return assets
