import subprocess
from portfolio_pulse.asset import Asset
from portfolio_pulse.broker_handler_woob import BrokerHandlerWoob


class BrokerHandlerDegiro(BrokerHandlerWoob):

    def _pass_command(self, command, password_entry):
        return subprocess.check_output(['pass', command, password_entry]).decode().strip().split('\n')[0]

    def get_login_data(self, broker_section):
        login = broker_section.get('login')
        password_entry = broker_section.get('password_entry')

        if not login or not password_entry:
            raise ValueError("Missing login or password entry in broker configuration.")

        password = self._pass_command('show', password_entry)
        pass_otp = self._pass_command('otp', password_entry)

        return {'login': login, 'password': password, 'otp': pass_otp}

    def process_investment(self, investment) -> Asset:
        """Processes investment data and assigns the appropriate category and values."""

        asset = super().process_investment(investment)
        return asset
