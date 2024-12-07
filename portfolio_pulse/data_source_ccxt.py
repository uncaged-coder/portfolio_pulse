import ccxt
from typing import List
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource


class DataSourceCcxt(DataSource):
    def __init__(self, broker_config_section):
        self.exchange_name = broker_config_section.get("broker", "unknown broker")
        self.api_key = broker_config_section.get("api_key")
        self.secret = broker_config_section.get("secret")
        self.exchange = self._initialize_exchange()

    def _initialize_exchange(self):
        """Initialize the exchange client using ccxt."""
        exchange_class = getattr(ccxt, self.exchange_name)
        exchange = exchange_class({
            'apiKey': self.api_key,
            'secret': self.secret,
            'enableRateLimit': True,
        })
        return exchange


    def _convert_to_eur(self, price: float, currency: str) -> float:
        """Converts the given price to EUR if it's in a non-EUR currency."""
        if currency == "EUR":
            return price
        elif currency == "USDT":
            eur_usdt_rate = self.exchange.fetch_ticker("EUR/USDT")['last']
            return price / eur_usdt_rate if eur_usdt_rate else price  # Fallback if rate not available
        elif currency == "USD":
            eur_usd_rate = self.exchange.fetch_ticker("EUR/USD")['last']
            return price / eur_usd_rate if eur_usd_rate else price  # Fallback if rate not available
        return price  # Fallback to return price if currency is unexpected

    def _get_equivalent_symbol(self, symbol):
        # ETH.B would be ETH, ETH2.S would be ETH, etc...
        symbol = symbol.split(".")[0]

        if symbol == "BETH" or symbol == "ETH2":
            return "ETH"
        elif symbol ==  "DOT28":
            return "DOT"
        elif symbol == "LDBNB":
            return "BNB"
        else:
            return symbol

    def _get_price_in_eur(self, symbol: str) -> float:
        """
        Try to get the price of the symbol in EUR, falling back to USDT and USD
        if necessary. Converts to EUR if the price is found in another currency.
        """
        target_currencies = ["EUR", "USDT", "USD"]

        symbol = self._get_equivalent_symbol(symbol)

        for target_currency in target_currencies:
            for pair_format in [f"{symbol}/{target_currency}", f"{target_currency}/{symbol}"]:
                try:
                    ticker = self.exchange.fetch_ticker(pair_format)

                    if ticker and ticker['last'] is None:
                        continue

                    price = ticker['last']
                    if pair_format == f"{symbol}/{target_currency}":
                        # Direct conversion if pair is in the form of symbol/target_currency
                        return self._convert_to_eur(price, target_currency)
                    else:
                        # Invert price if pair is in the form of target_currency/symbol
                        return self._convert_to_eur(1 / price, target_currency)

                except ccxt.BaseError:
                    continue

        raise ValueError(f"Could not fetch price for {symbol} in EUR, USDT, or USD.")

    def fetch_assets(self) -> List[Asset]:
        """Fetch crypto assets from the specified exchange."""
        assets = []
        balance_data = self.exchange.fetch_balance()

        for symbol, balance in balance_data['total'].items():
            if balance <= 0:
                continue

            try:
                price_in_eur = self._get_price_in_eur(symbol)
                if price_in_eur < 1:
                    continue
                asset = Asset(
                    name=symbol,
                    broker=self.exchange_name,
                    isin="",  # Cryptos don't have ISINs
                    category="Crypto",
                    quantity=balance,
                    price=price_in_eur
                )
                assets.append(asset)
            except ValueError as e:
                print(f"Warning: Could not fetch price for {symbol}. Error: {e}")

        return assets
