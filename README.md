# Portfolio Pulse

**Portfolio Pulse** is a command-line tool that aggregates and analyzes your investment holdings from multiple sources, compares them to your target allocation model, and helps you identify opportunities to rebalance. Whether you follow a standard portfolio like an All-Weather mix or something more specialized like a Gave-inspired defensive strategy, Portfolio Pulse can keep you on track.

## Key Features

- **Multi-Source Integration:** Pull data from brokers and platforms via Woob, CCXT, CSV, or IBKR APIs.
- **Customizable Allocations:** Define your target percentages and "good" assets for each category (e.g., Gold, Stocks, Energy Stocks, Currencies, Crypto).
- **Real-Time Comparison:** Instantly compare actual asset distribution vs. your target model and see which categories need attention.
- **Categorization via Config Files:** Easily manage categories, ISINs, and symbols in separate config files for flexibility without code changes.

## Setup

1. **Configuration Files:**
   All configurations live under `~/.config/portfolio_pulse/`:
   - **User Config:** `~/.config/portfolio_pulse/<user>.ini` defines accounts, credentials, and data sources.
   - **Model Allocation:** `~/.config/portfolio_pulse/model_<modelname>.ini` sets target percentages and "good" assets.
   - **Stock Category:** `~/.config/portfolio_pulse/stock_category.ini` maps ISINs and symbols to categories (e.g., Gold, Energy).

2. **Install Dependencies:**
   - Python 3 and required packages.
   - Additional setups may be required for Woob or CCXT usage.

## Example Configurations

**Model Allocation (`model_gave2_default.ini`):**
```ini
[Gold]
target_percentage = 25
good_assets = US1234567890

[Currencies]
target_percentage = 25

[Stocks]
target_percentage = 25
good_assets = US0378331005, FR0000131906

[Energie Stocks]
target_percentage = 25

[Bonds]
target_percentage = 0

[Crypto]
target_percentage = 0
good_assets = BTC
```

**User Accounts (user.ini):**

```ini
[boursorama]
type = woob
login = 11223344
password_entry = user/perso/finance/boursorama.com/11223344

[bullionstar]
type = woob
login = xx@gmail.com
password_entry = user/perso/finance/bullionstar.com/xx@gmail.com

[degiro]
type = woob
login = xx
password_entry = user/perso/finance/degiro.nl/xx

[csv]
type = csv
file = /data/portfolio_pulse/private/user.csv

[binance]
broker = binance
type = ccxt
api_key = aaaaaaaaaaaaaaaaaaaaaaaa
secret = aaaaaaaaaaaa
```

**Stock Categories (stock_category.ini):**

```ini

[Gold]
ISINS = DE000A0S9GB0,CH0047533523,CH0183136057
SYMBOLS = ZSILEU,ZGLDEU

[Energies]
ISINS = FR0000120271,GA0000121459,FR0000051070,JE00B55Q3P39,GB0007188757,US3682872078,US69343P1057,US88642R1095,LT0000128621,US71654V4086,IE00BM67HM91
SYMBOLS = EC,GAZ,LKOD,LUK.EUR,SEPL,RIO,PKN,MAU,XDW0

```

## Usage

Run the tool by specifying the user and model:

```bash
python3 portfolio_pulse.py --user user --model gave2_default
```

This will:

- Fetch all assets from sources defined in user.ini.
- Load and compare against the allocations in model_gave2_default.ini.
- Print a detailed and a concise report showing actual vs. target allocations and highlight good assets.

## Rebalancing Strategy

Use the reports to see if you need to add or remove assets to meet your target allocations. Over time, as markets shift, Portfolio Pulse helps you maintain your desired balance, ensuring your portfolio remains aligned with your strategy.
