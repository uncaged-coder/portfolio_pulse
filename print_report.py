from portfolio_pulse.portfolio_model import PortfolioModel
from portfolio_pulse.asset import Asset
from portfolio_pulse.allocation import Allocation
from portfolio_pulse.report_generator_console import ReportGeneratorConsole


if __name__ == "__main__":
    # Setup test portfolio model
    allocations = {
        "Gold": Allocation(25, ["US1234567890"]),
        "Stocks": Allocation(50, ["US0378331005", "FR0000131906"]),
        "Bonds": Allocation(15),
        "Crypto": Allocation(10, ["BTC"]),
    }

    portfolio_model = PortfolioModel(allocations)
    portfolio_model.classify_asset(Asset("Gold ETF", "US1234567890", "Gold", 1800, 2))
    portfolio_model.classify_asset(Asset("Apple Inc", "US0378331005", "Stocks", 150, 10))
    portfolio_model.classify_asset(Asset("Renault", "FR0000131906", "Stocks", 40, 20))
    portfolio_model.classify_asset(Asset("Bitcoin", "BTC", "Crypto", 30000, 0.5))

    # Generate and print console report
    report = ReportGeneratorConsole(portfolio_model)
    print(report.generate_report())
