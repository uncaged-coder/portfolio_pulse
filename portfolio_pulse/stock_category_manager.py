import os
import configparser


CONFIG_PATH = os.path.expanduser("~/.config/portfolio_pulse/stock_category.ini")


class StockCategoryManager:
    def __init__(self, config_path=CONFIG_PATH):
        self.categories = {}
        self._load_config(config_path)

    def _load_config(self, config_path):
        # Initialize a parser
        config = configparser.ConfigParser()
        if not os.path.exists(config_path):
            print(f"Warning: Config file not found at {config_path}. Using empty config.")
            return

        config.read(config_path)

        # For each section, read the ISINS and SYMBOLS
        for section in config.sections():
            isins = []
            symbols = []
            if config.has_option(section, "ISINS"):
                isins = [i.strip() for i in config.get(section, "ISINS").split(",") if i.strip()]
            if config.has_option(section, "SYMBOLS"):
                symbols = [s.strip() for s in config.get(section, "SYMBOLS").split(",") if s.strip()]

            self.categories[section.lower()] = {
                "isins": set(isins),
                "symbols": set(symbols)
            }

    def is_isin_in_category(self, isin: str, category: str) -> bool:
        category_data = self.categories.get(category.lower())
        if category_data is None:
            return False
        return isin in category_data["isins"]

    def is_symbol_in_category(self, symbol: str, category: str) -> bool:
        category_data = self.categories.get(category.lower())
        if category_data is None:
            return False
        return symbol in category_data["symbols"]

    def get_category_from_isin(self, isin: str) -> str:
        for category, data in self.categories.items():
            if isin in data["isins"]:
                return category
        return None

    def get_category_from_symbol(self, symbol: str) -> str:
        for category, data in self.categories.items():
            if symbol in data["symbols"]:
                return category
        return None

# Example usage:
# manager = StockCategoryManager()
# if manager.is_isin_in_category("DE000A0S9GB0", "Gold"):
#     print("This ISIN corresponds to a gold asset.")
# category = manager.get_category_from_symbol("ZSILEU")
# if category == "gold":
#     print("This symbol corresponds to a gold asset.")
