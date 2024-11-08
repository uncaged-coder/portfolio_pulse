from typing import List


# Class representing a specific allocation target for each asset class
class Allocation:
    def __init__(self, target_percentage: float, good_assets: List[str] = None):
        self.target_percentage = target_percentage
        self.good_assets = good_assets or []

    def is_good_asset(self, isin: str) -> bool:
        """Check if an asset with the given ISIN is considered 'good'."""
        return isin in self.good_assets
