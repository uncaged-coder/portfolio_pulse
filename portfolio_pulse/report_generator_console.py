from portfolio_pulse.report_generator import ReportGenerator


class ReportGeneratorConsole(ReportGenerator):
    def generate_report(self) -> str:
        """Generate a console-friendly report."""
        summary_lines = ["Portfolio Summary:"]
        total_value = self.portfolio_model.total_portfolio_value()
        actual_weights = self.portfolio_model.calculate_actual_weights()
        asset_status = self.portfolio_model.get_asset_status()

        for category, allocation in self.portfolio_model.allocations.items():
            actual_weight = actual_weights.get(category, 0)
            delta = actual_weight - allocation.target_percentage
            summary_lines.append(
                f"{category}: {actual_weight:.2f}% (Target: {allocation.target_percentage}%, "
                f"Delta: {delta:+.2f}%)"
            )

            for asset, status in asset_status.get(category, []):
                summary_lines.append(
                    f"  - {asset.name} ({asset.isin}): {asset.value():.2f} ({status})"
                )

        return "\n".join(summary_lines)
