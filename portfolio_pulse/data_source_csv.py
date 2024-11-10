import os
import json
import datetime
import math
from pathlib import Path
from typing import Dict, List, Union
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource
from yahoo_fin import stock_info as si


class DataSourceCSV(DataSource):
    def __init__(self, config_section: str):
        self.file_name = config_section.get('file')
        self.cache_file = str(Path("~/.cache/portfolio_pulse/price_cache.json").expanduser())
        isin_map_file = "~/.config/portfolio_pulse/isin_map.ini"
        self.isin_map_file = str(Path(isin_map_file).expanduser())
        self.cache = self._load_cache()
        self.isin_to_symbol_map = self._load_isin_map()

    def _load_isin_map(self) -> Dict[str, tuple[str, str]]:
        """Load ISIN-to-symbol and currency mapping from the configuration file."""
        isin_map = {}
        if os.path.exists(self.isin_map_file):
            with open(self.isin_map_file, "r") as file:
                for line in file:
                    line = line.strip()
                    if "=" in line and ":" in line:
                        isin, mapping = line.split("=")
                        symbol, currency = mapping.split(":")
                        isin_map[isin.strip()] = (symbol.strip(), currency.strip())
        return isin_map

    def _load_cache(self) -> Dict:
        """Load cached prices from a file in the user cache directory."""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)  # Ensure the cache directory exists
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as file:
                return json.load(file)
        return {}

    def _save_cache(self):
        """Save cached prices to a file in the user cache directory."""
        with open(self.cache_file, "w") as file:
            json.dump(self.cache, file)

    def _is_cache_valid(self, symbol: str) -> bool:
        """Check if cache for a given symbol is still valid (within 2 days)."""
        if symbol in self.cache:
            cache_date = datetime.datetime.strptime(self.cache[symbol]['date'], "%Y-%m-%d")
            return (datetime.datetime.now() - cache_date).days < 2
        return False

    def _convert_to_currency(self, price, from_currency, to_currency):
        # we use EUR currencie
        if from_currency == to_currency:
            return price

        # other currencies are quoted in USD, get USD price
        if from_currency != "USD":
            conversion_rate = self._get_price(f"{from_currency}USD=X")
            price *= conversion_rate
        # convert in EUR
        conversion_rate = self._get_price(f"{to_currency}USD=X")
        price /= conversion_rate
        return price

    def _get_price_from_yahoo(self, symbol: str) -> float:
        """Fetch price from Yahoo Finance."""
        try:
            return si.get_live_price(symbol)

        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return 0.0

    def _get_price(self, symbol: str) -> float:
        """Get price from cache or Yahoo Finance if cache is outdated or missing."""
        if not self._is_cache_valid(symbol):
            price = self._get_price_from_yahoo(symbol)
            self.cache[symbol] = {"price": price, "date": datetime.datetime.now().strftime("%Y-%m-%d")}
            self._save_cache()
        price = self.cache[symbol]["price"]
        if math.isnan(price):
            return 0
        else:
            return price

    def isin_to_symbol(self, isin: str) -> tuple[str, str]:
        """Convert ISIN to stock symbol and currency using the predefined mapping."""
        return self.isin_to_symbol_map.get(isin, ("", ""))

    def fetch_assets(self) -> List[Asset]:
        assets = []
        with open(self.file_name, "r") as file:
            for line in file.readlines()[1:]:  # Skip header
                isin, name, category, quantity, buy_price, broker, date, unit_price, currency = line.strip().split(',')
                category = category.strip()
                currency = currency.strip()
                name = name.strip()
                unit_price = unit_price.strip()
                symbol = ""

                # Determine symbol based on category and fetch the price
                if category == "Crypto":
                    symbol = isin + "-USD"  # For crypto, ISIN is the symbol itself
                    currency = "USD"
                elif category in ["Stock", "Energie Stocks"]:
                    symbol, currency = self.isin_to_symbol(isin)
                elif category == "Gold":
                    symbol = "GC=F"
                    currency = "USD"
                elif category == "Silver":
                    symbol = "SI=F"
                    category = "Gold"
                    currency = "USD"
                elif category == "Currencies":
                    pass
                else:
                    symbol = None

                if symbol:
                    # price are valued in currency
                    unit_price = self._get_price(symbol)

                # convert to euro
                if unit_price and currency:
                    if currency == "NA":
                        currency = "EUR"
                    elif currency != "EUR":
                        unit_price = self._convert_to_currency(unit_price, currency, "EUR")

                assets.append(Asset(name, broker, isin, category, float(quantity), float(unit_price)))
        return assets
