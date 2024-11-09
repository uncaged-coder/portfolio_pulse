from portfolio_pulse.asset import Asset
from portfolio_pulse.broker_handler import BrokerHandler
from portfolio_pulse.broker_handler_energies_stock import is_energy_stock
from portfolio_pulse.broker_handler_gold_stock import is_gold_stock
from decimal import Decimal
import subprocess
from woob.capabilities.base import NotAvailableType


class BrokerHandlerWoob(BrokerHandler):

    def get_login_data(self, broker_section):
        login = broker_section.get('login')
        password_entry = broker_section.get('password_entry')

        if not login or not password_entry:
            raise ValueError("Missing login or password entry in broker configuration.")

        password = subprocess.check_output(['pass', password_entry]).decode().strip().split('\n')[0]
        return {'login': login, 'password': password}

    def process_investment(self, investment) -> Asset:
        """Processes investment data and assigns the appropriate category and values."""

        def to_float(value):
            return float(value) if isinstance(value, Decimal) else value

        name = investment.label
        isin = investment.code

        if isin == "XX-liquidity":
            category = "Currencies"
            unit_price = 1.0
            quantity = to_float(investment.valuation)
        else:
            if is_energy_stock(isin):
                category = "Energie Stocks"
            elif is_gold_stock(isin):
                category = "Gold"
            else:
                category = "Stocks"
            quantity = to_float(investment.quantity)

            # Check if unitprice is available; if not, calculate it
            if isinstance(investment.unitprice, NotAvailableType):
                if investment.quantity != Decimal('0'):
                    unit_price = to_float(investment.valuation / investment.quantity)
                else:
                    unit_price = None
            else:
                unit_price = to_float(investment.unitprice)

        return Asset(
            name=name,
            isin=isin,
            category=category,
            quantity=quantity,
            price=unit_price
        )