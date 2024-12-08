from portfolio_pulse.report_generator import ReportGenerator
from collections import defaultdict


class ReportGeneratorConsole(ReportGenerator):
    # Define some ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BLUE = "\033[34m"

    def generate_report(self, verbose: bool = True) -> str:
        """Generate a console-friendly report with optional verbosity."""
        total_value = self.portfolio_model.total_portfolio_value()

        summary_lines = [
            f"{self.BOLD}{self.CYAN}========={self.RESET}",
            f"{self.BOLD}Portfolio Summary (total={total_value:.2f}) :{self.RESET}"
        ]

        actual_weights = self.portfolio_model.calculate_actual_weights()
        asset_status = self.portfolio_model.get_asset_status()

        for category, allocation in self.portfolio_model.allocations.items():
            actual_weight = actual_weights.get(category, 0.0)
            delta = actual_weight - allocation.target_percentage

            # Calculate good asset percentage within the category
            category_assets = asset_status.get(category, [])
            category_total_value = sum(asset.value() for asset, _ in category_assets)
            good_total_value = sum(asset.value() for asset, status in category_assets if status == "Good")
            good_percentage = (good_total_value / category_total_value * 100) if category_total_value > 0 else 0

            # Calculate broker distribution within the category
            broker_values = defaultdict(float)
            for asset, _status in category_assets:
                broker_values[asset.broker] += asset.value()

            # Choose a color for delta
            if delta > 0:
                delta_color = self.GREEN
            elif delta < 0:
                delta_color = self.RED
            else:
                delta_color = self.YELLOW

            summary_lines.append(
                f"{self.BOLD}{self.BLUE}{category}{self.RESET}: {actual_weight:.2f}% "
                f"(Target: {allocation.target_percentage}%, "
                f"Delta: {delta_color}{delta:+.2f}%{self.RESET})"
            )

            # Print the percentage of good assets in this category
            good_color = self.GREEN if good_percentage >= 50 else self.YELLOW
            summary_lines.append(f"  Good assets in {category}: {good_color}{good_percentage:.2f}%{self.RESET}")

            # If verbose, print more details
            if verbose:
                # Print broker distribution
                for broker, val in broker_values.items():
                    broker_percentage = (val / category_total_value * 100) if category_total_value > 0 else 0
                    summary_lines.append(
                        f"    Broker: {self.CYAN}{broker}{self.RESET}: {broker_percentage:.2f}% of {category}"
                    )

                # Print each asset
                for asset, status in category_assets:
                    status_color = self.GREEN if status == "Good" else self.RED
                    summary_lines.append(
                        f"  - {asset.name} ({asset.isin}, {asset.broker}): {asset.value():.2f} "
                        f"({status_color}{status}{self.RESET})"
                    )

        return "\n".join(summary_lines)
