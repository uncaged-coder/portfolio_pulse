import json
import os
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.utils import iswrapper
from typing import List
import threading
import time
from portfolio_pulse.asset import Asset
from portfolio_pulse.data_source import DataSource
from portfolio_pulse.stock_category_manager import StockCategoryManager


EXCHANGE_RATE_FILE = "data/ibkr_exchange_rates.json"


class IBKRClient(EWrapper, EClient):
    def __init__(self, broker):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        self.broker = broker
        self.assets = []
        self.positions_ready = threading.Event()
        self._price = {}
        self._using_temp_price = False
        self.currency = None

        # Event to indicate that we've received at least one cash balance update
        self.cash_balances_updated = threading.Event()
        self.cash_balances = {}

    def error(self, reqId, errorCode, errorString):
        # Handle known non-critical errors
        if errorCode in [2104, 2106, 2158]:
            # Informational market data messages
            return
        elif errorCode == 200:
            # No security definition found - set price to 0.
            self._price[reqId] = 0
        elif errorCode == 354:
            # Requested market data not subscribed - set price to 0.
            self._price[reqId] = 0
        else:
            print(f"Error: ReqId={reqId}, Code={errorCode}, Msg={errorString}")

    def _get_category(self, sec_type):
        if sec_type == "STK":
            return "Stocks"
        elif sec_type == "CASH":
            return "Currencies"
        else:
            raise ValueError(f"Unsupported security type: {sec_type}")

    @iswrapper
    def tickPrice(self, reqId, tickType, price, attrib):
        # Filter out invalid prices
        if price is None or price <= 0:
            return

        # Prefer tickType=4 (last bid). Otherwise, accept delayed prices if we have none yet.
        if tickType == 4:
            self._price[reqId] = price
            self._using_temp_price = False
        elif tickType in [9, 68, 75] and (self._price[reqId] is None or self._using_temp_price):
            self._price[reqId] = price
            self._using_temp_price = False
        elif self._price[reqId] is None:
            self._price[reqId] = price
            self._using_temp_price = True

    @iswrapper
    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        category = self._get_category(contract.secType)
        asset = Asset(contract.symbol, self.broker, contract.symbol, category, position, None)
        asset.initial_currency = contract.currency
        self.assets.append(asset)

    @iswrapper
    def positionEnd(self):
        self.positions_ready.set()

    @iswrapper
    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        # This callback is triggered by reqAccountUpdates()
        # CashBalance should provide a line per currency
        if key == "CashBalance":
            self.cash_balances[currency] = float(val)
            self.cash_balances_updated.set()  # We got at least one cash balance update


class DataSourceIBKR(DataSource):
    def __init__(self, config_section: dict):
        self.broker = config_section.get("broker", "unknown broker")
        self.host = "127.0.0.1"
        self.port = 7496
        self.client_id = 0
        self.client = IBKRClient(self.broker)
        self.connected = False
        self.req_id = 1

         # Load previously known exchange rates
        self.exchange_rates = self.load_exchange_rates()

    def load_exchange_rates(self):
        if os.path.isfile(EXCHANGE_RATE_FILE):
            with open(EXCHANGE_RATE_FILE, "r") as f:
                data = json.load(f)
                # Ensure no zero rates stored
                return {k: v for k, v in data.items() if v != 0}
        return {}

    def save_exchange_rates(self):
        # Save only non-zero rates
        cleaned = {k: v for k, v in self.exchange_rates.items() if v != 0}
        os.makedirs("data", exist_ok=True)
        with open(EXCHANGE_RATE_FILE, "w") as f:
            json.dump(cleaned, f, indent=2)

    def _connect(self):
        if not self.client.isConnected():
            self.client.connect(self.host, self.port, self.client_id)
            thread = threading.Thread(target=self.client.run, daemon=True)
            thread.start()
            time.sleep(1)
            if self.client.isConnected():
                self.connected = True
                print("Connected to IBKR")

    def _disconnect(self):
        if self.client.isConnected():
            self.client.disconnect()
            self.connected = False
            print("Disconnected from IBKR")

            self.save_exchange_rates()

    def _get_price(self, symbol, sec_type, exchange, currency):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.currency = currency
        contract.exchange = exchange

        self.req_id += 1
        rid = self.req_id
        self.client._price[rid] = None
        self.client._using_temp_price = False

        self.client.reqMarketDataType(3)  # delayed data if necessary
        self.client.reqMktData(rid, contract, '', True, False, [])

        timeout = time.time() + 5
        while self.client._price[rid] is None and time.time() < timeout:
            time.sleep(0.1)

        self.client.cancelMktData(rid)  # Stop receiving data

        if self.client._price[rid] is None:
            print(f"Issue retrieving price for {symbol}, setting to 0.")
            return 0.0

        return self.client._price[rid]

    def get_exchange_rate(self, from_currency, to_currency='EUR'):
        if from_currency == 'EUR':
            return 1.0

        # If we already have a valid exchange rate and market data might not be available now:
        if from_currency in self.exchange_rates and self.exchange_rates[from_currency] != 0:
            cached_rate = self.exchange_rates[from_currency]
        else:
            cached_rate = None

        # Attempt to get a fresh rate from IBKR
        fresh_rate = self._get_price(from_currency, "CASH", "IDEALPRO", to_currency)
        if fresh_rate == 0.0:
            # If fresh rate is zero, fallback to cached if available
            if cached_rate is not None:
                print(f"Warning: IBKR returned 0 for {from_currency}, using cached rate {cached_rate}")
                return cached_rate
            else:
                print(f"Warning: No fresh or cached exchange rate for {from_currency}. Returning 0.")
                return 0.0
        else:
            # Update and store the new non-zero rate
            self.exchange_rates[from_currency] = fresh_rate
            return fresh_rate

    def convert_to_eur(self, amount, currency):
        exchange_rate = self.get_exchange_rate(currency)
        if exchange_rate == 0:
            breakpoint()
            raise ValueError(f"exchange_rate is zero for {currency}")

        # Special handling for GBP if needed
        if currency == "GBP":
            exchange_rate /= 100
        return amount * exchange_rate

    def get_price(self, symbol, currency):
        price = self._get_price(symbol, "STK", "SMART", currency)
        price2 = self.convert_to_eur(price, currency)
        return price2

    def update_cash_balances(self, timeout=5.0):
        """
        Request account updates to populate cash_balances with per-currency values.
        Wait for at least one balance update or raise TimeoutError.
        """
        if not self.connected:
            self._connect()

        # Clear current balances and reset event
        self.client.cash_balances.clear()
        self.client.cash_balances_updated.clear()

        # Start receiving account updates
        self.client.reqAccountUpdates(True, "All")

        # Wait until we get at least one cash balance or time out
        start_time = time.time()
        while not self.client.cash_balances_updated.is_set():
            if time.time() - start_time > timeout:
                # Stop updates and raise error
                self.client.reqAccountUpdates(False, "All")
                raise TimeoutError("Timed out waiting for cash balances from IBKR.")
            time.sleep(0.1)

        # Once we have at least one update, we can stop receiving updates.
        # However, IBKR may send multiple currency lines in quick succession.
        # Wait a short moment to let all arrive.
        time.sleep(1)
        self.client.reqAccountUpdates(False, "All")

    def fetch_assets(self) -> List[Asset]:
        if not self.connected:
            self._connect()

        # Update the cash balances first
        self.update_cash_balances()

        # Now we have a dictionary of currency: amount
        assets = []
        for currency, amount in self.client.cash_balances.items():
            # this is the total
            if currency == "BASE":
                continue

            amount_in_eur = self.convert_to_eur(amount, currency)
            assets.append(Asset(currency, self.broker, currency, "Currencies", 1, amount_in_eur))

        self.client.positions_ready.clear()
        self.client.reqPositions()
        self.client.positions_ready.wait()

        classifier = StockCategoryManager()

        for a in self.client.assets:
            if classifier.is_symbol_in_category(a.name, "Energies"):
                category = "Energie Stocks"
            elif classifier.is_symbol_in_category(a.name, "Gold"):
                category = "Gold"
            elif a.category == "Currencies":
                category = "Currencies"
            else:
                category = "Stocks"

            a.category = category
            a.price = self.get_price(a.name, a.initial_currency)
            assets.append(a)

        self._disconnect()
        return assets
