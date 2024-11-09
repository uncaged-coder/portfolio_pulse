from portfolio_pulse.asset import Asset
from portfolio_pulse.portfolio_model import PortfolioModel
from portfolio_pulse.allocation import Allocation
from portfolio_pulse.account_manager import AccountManager
from portfolio_pulse.report_generator_console import ReportGeneratorConsole


# Define target allocations and good assets
gave_etf_allocations = {
    "Gold": Allocation(25, ["US1234567890"]),
    "Currencies": Allocation(25, []),
    "Stocks": Allocation(25, ["US0378331005", "FR0000131906"]),
    "Energie Stocks": Allocation(25, []),
    "Bonds": Allocation(0),
}
uncaged_allocations = {
    "Gold": Allocation(25, ["US1234567890"]),
    "Currencies": Allocation(0, []),
    "Stocks": Allocation(23, ["US0378331005", "FR0000131906"]),
    "Energie Stocks": Allocation(23, []),
    "Bonds": Allocation(21),
    "Crypto": Allocation(8, ["BTC"]),
}

account_config = {
    "woob": {"type": "woob"},
}

if __name__ == "__main__":

    # Initialize portfolio model with target allocations
    portfolio = PortfolioModel(uncaged_allocations)

    manager = AccountManager(account_config)
    all_assets = manager.fetch_all_assets()

    for account, assets in all_assets.items():
        print(f"Assets for {account}:")
        for asset in assets:
            print(f"  - {asset.name} ({asset.isin}): {asset.category}, {asset.quantity}x{asset.price}")
            portfolio.classify_asset(asset)


    report = ReportGeneratorConsole(portfolio)

    # Print portfolio summary
    #print(portfolio.get_asset_status())
    out=report.generate_report()
    print(out)
