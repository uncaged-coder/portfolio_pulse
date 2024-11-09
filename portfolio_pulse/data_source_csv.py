from typing import List
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource


class DataSourceCSV(DataSource):
    def __init__(self, config_section: str):
        self.file_name = config_section.get('file')

    def fetch_assets(self) -> List[Asset]:
        assets = []
        with open(self.file_name, "r") as file:
            for line in file.readlines()[1:]:  # Skip header
                isin, name, category, quantity, buy_price, broker, date, unit_price = line.strip().split(',')
                category = category.strip()
                if category == "Silver":
                    category = "Gold"
                assets.append(Asset(name, broker, isin, category, float(quantity), float(unit_price)))
        return assets
