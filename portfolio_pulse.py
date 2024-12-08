import os
import sys
import configparser
from portfolio_pulse.asset import Asset
from portfolio_pulse.portfolio_model import PortfolioModel
from portfolio_pulse.allocation import Allocation
from portfolio_pulse.account_manager import AccountManager
from portfolio_pulse.report_generator_console import ReportGeneratorConsole


def load_model_allocations(model: str):
    """
    Load the model allocation configuration from the specified file.
    Defaults to 'model_default.ini' if no specific model name is provided.
    """
    config_path = os.path.expanduser(f"~/.config/portfolio_pulse/model_{model}.ini")
    if not os.path.exists(config_path):
        print(f"Model file '{config_path}' not found. Exiting.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)

    allocations = {}
    for section in config.sections():
        target_percentage = config.getfloat(section, "target_percentage", fallback=0)
        good_assets = config.get(section, "good_assets", fallback="").split(",")
        good_assets = [asset.strip() for asset in good_assets if asset.strip()]
        allocations[section] = Allocation(target_percentage, good_assets)

    return allocations


if __name__ == "__main__":
    import argparse

    # Parse command-line arguments for user and model
    parser = argparse.ArgumentParser(description="Portfolio Pulse Analysis")
    parser.add_argument("--user", type=str, help="Specify the user for account management.")
    parser.add_argument("--model", type=str, default="default", help="Specify the portfolio model name to load allocations.")
    args = parser.parse_args()

    # Check if user argument was provided
    if args.user is None:
        print("Error: The '--user' argument is required.")
        parser.print_help()
        sys.exit(1)

    # Load allocations based on the specified model
    model_allocations = load_model_allocations(args.model)
    portfolio = PortfolioModel(model_allocations)

    # Initialize account manager with the specified user
    manager = AccountManager(args.user)
    all_assets = manager.fetch_all_assets()

    for account, assets in all_assets.items():
        print(f"Assets for {account}:")
        for asset in assets:
            print(f"  - {asset.name} ({asset.isin}): {asset.category}, {asset.quantity}x{asset.price}")
            portfolio.classify_asset(asset)

    # Generate and print report
    report = ReportGeneratorConsole(portfolio)
    out = report.generate_report(verbose=True)
    print(out)
    print("==============")
    out = report.generate_report(verbose=False)
    print(out)
