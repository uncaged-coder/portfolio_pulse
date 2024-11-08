from collections import defaultdict
from typing import Dict, List, Tuple
from portfolio_pulse.allocation import Allocation
from portfolio_pulse.asset import Asset


class PortfolioModel:
    def __init__(self, allocations: Dict[str, Allocation]):
        self.allocations = allocations
        self.assets = defaultdict(list)

    def classify_asset(self, asset: Asset):
        if asset.category not in self.allocations:
            print(f"Warning: Asset {asset.name} has an undefined category '{asset.category}'")
        self.assets[asset.category].append(asset)

    def total_portfolio_value(self) -> float:
        return sum(asset.value() for assets in self.assets.values() for asset in assets)

    def calculate_actual_weights(self) -> Dict[str, float]:
        total_value = self.total_portfolio_value()
        return {
            category: (sum(asset.value() for asset in assets) / total_value * 100) if total_value > 0 else 0
            for category, assets in self.assets.items()
        }

    def get_asset_status(self) -> Dict[str, List[Tuple[Asset, str]]]:
        """Return a dictionary with assets and their 'Good' or 'Not Good' status."""
        asset_status = {}
        for category, assets in self.assets.items():
            allocation = self.allocations.get(category)
            asset_status[category] = [
                (asset, "Good" if allocation and allocation.is_good_asset(asset.isin) else "Not Good")
                for asset in assets
            ]
        return asset_status
