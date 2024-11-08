from portfolio_pulse.asset import Asset
from portfolio_pulse.portfolio_model import PortfolioModel
from portfolio_pulse.allocation import Allocation


# Usage Example
if __name__ == "__main__":
    # Define target allocations and good assets
    allocations = {
        "Gold": Allocation(25, ["US1234567890"]),
        "Stocks": Allocation(50, ["US0378331005", "FR0000131906"]),
        "Bonds": Allocation(15),
        "Crypto": Allocation(10, ["BTC"]),
    }

    # Initialize portfolio model with target allocations
    portfolio = PortfolioModel(allocations)

    # Add some assets to the portfolio
    portfolio.classify_asset(Asset("Gold ETF", "US1234567890", "Gold", 1800, 2))
    portfolio.classify_asset(Asset("Apple Inc", "US0378331005", "Stocks", 150, 10))
    portfolio.classify_asset(Asset("Renault", "FR0000131906", "Stocks", 40, 20))
    portfolio.classify_asset(Asset("Pigo", "FR00001312222", "Stocks", 40, 20))
    portfolio.classify_asset(Asset("Bitcoin", "BTC", "Crypto", 30000, 0.5))

    # Print portfolio summary
    print(portfolio.get_asset_status())
