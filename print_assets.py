from portfolio_pulse.account_manager import AccountManager


# Usage Example
if __name__ == "__main__":
    account_config = {
        "Account1": {"type": "csv", "file_path": "assets.csv"},
        "Account2": {"type": "woob"},
    }
    manager = AccountManager(account_config)
    all_assets = manager.fetch_all_assets()

    for account, assets in all_assets.items():
        print(f"Assets for {account}:")
        for asset in assets:
            print(f"  - {asset.name} ({asset.isin}): {asset.category}, {asset.quantity}x{asset.price}")
