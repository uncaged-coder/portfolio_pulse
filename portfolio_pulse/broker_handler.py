from abc import ABC, abstractmethod
from portfolio_pulse.asset import Asset


class BrokerHandler(ABC):
    """Base class for handling broker-specific asset processing adjustments."""

    def __init__(self, broker_name: str):
        self.broker_name = broker_name

    @abstractmethod
    def get_login_data(self, broker_section):
        pass

    @abstractmethod
    def process_investment(self, investment) -> Asset:
        """Process an investment and return an Asset. Can be overridden by specific brokers."""
        pass
