# Portfolio Pulse

**Portfolio Pulse** is a Python script to gather and track your investment data, making it easier to monitor your portfolio’s performance. If you maintain a diversified portfolio, such as an *All-Weather Portfolio* or one inspired by *Gave’s Defensive Portfolio*, this tool will help you ensure your asset allocations remain balanced and aligned with your target percentages. 

By integrating data from multiple sources, **Portfolio Pulse** provides real-time insights on your portfolio composition and highlights when rebalancing is needed.

## Portfolio Types

### Example: All-Weather Portfolio
This popular portfolio type typically includes:
- **50% Stocks** (e.g., SP500, CAC40, MSCI, etc.)
- **25% Gold**
- **25% Bonds** (e.g., US, German, or Chinese bonds)

### Example: Gave’s Defensive Portfolio
The Gave Portfolio is designed to be resilient and defensive, with allocations like:
- **25% Energy Stocks**
- **25% Gold**
- **25% Yen** (or similar currency assets)
- **25% Asian Stocks** (excluding Japan, includes India)

### My Customized Portfolio
Inspired by Gave’s portfolio, my allocation also includes cryptocurrencies, with periodic adjustments to account for BTC and other crypto assets.

## Rebalancing Strategy

Every three months (or a similar interval), I review my asset distribution to ensure it aligns with my target allocations. Earnings from freelance work are invested in underweighted assets, and if disparities are significant, I rebalance by selling overweight assets and buying underweight ones.

## Features

Using **Portfolio Pulse**, you can:
1. **Quickly see asset allocations** relative to your target percentages.
2. **Pull data** from various sources:
   - **[Woob](https://woob.tech/)** (Web Outside of Browser) for banking and gold data.
   - **[CCXT](https://github.com/ccxt/ccxt)** for real-time cryptocurrency data from online brokers.
   - Local CSV files for crypto assets and other holdings not accessible via Woob or CCXT.

## Configuration

Configuration files are stored in `~/.config/portfolio_pulse/`. Each account or portfolio provider has its own `.ini` file specifying login credentials, data sources, and target portfolio models.

### Account Configuration Example

```ini
# ~/.config/portfolio_pulse/account1.ini

[boursorama]
type = woob
login = 11223344
password_entry = finance/boursorama.com/11223344

[degiro]
type = woob
login = xxx
password_entry = finance/degiro.nl/xxx

[binance]
broker = binance
type = ccxt
api_key = xxxxxx
secret = xxxxxxxxxx
```

_Note_:

- Credentials are securely managed via pass (password manager), where password_entry refers to the pass path for login credentials.
- OTP (one-time password) is also supported via pass, using the same entry as the password.

### Model Portfolio Configuration Example

Define your target portfolio in an .ini file like the one below (following the Gave Portfolio model):


```ini
# ~/.config/portfolio_pulse/gave2_default.ini

[Gold]
target_percentage = 25

[Currencies]
target_percentage = 25

[Stocks]
target_percentage = 25

[Energy Stocks]
target_percentage = 25

[Bonds]
target_percentage = 0

[Crypto]
target_percentage = 0
```

## Running Portfolio Pulse

To execute the script and get a snapshot of your portfolio’s allocation:

```bash
python3 portfolio_pulse.py --user account1 --model gave2

```

Here:
- --user specifies the account configuration (e.g., account1.ini).
- --model specifies the target portfolio configuration (e.g., gave2_default.ini).

This tool provides a simple, efficient, and secure way to keep your investments aligned with your strategy.
Happy investing!
