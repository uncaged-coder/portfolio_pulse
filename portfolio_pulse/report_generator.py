from abc import ABC, abstractmethod
from portfolio_pulse.portfolio_model import PortfolioModel


class ReportGenerator(ABC):
    def __init__(self, portfolio_model: 'PortfolioModel'):
        self.portfolio_model = portfolio_model

    @abstractmethod
    def generate_report(self) -> str:
        """Abstract method to generate a report."""
        pass
