from abc import ABC, abstractmethod
import configparser
from typing import List, Dict
from portfolio_pulse.asset import Asset


class DataSource(ABC):
    @abstractmethod
    def fetch_assets(self) -> List[Asset]:
        pass
