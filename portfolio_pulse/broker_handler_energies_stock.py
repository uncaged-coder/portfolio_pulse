ENERGY_STOCK_ISINS = {
    "FR0000120271", # Total energies
    "GA0000121459", # Total Gabon
    "FR0000051070", # Maurel & Prom 
    "JE00B55Q3P39", # Genel Energy PLC
    "GB0007188757", # Rio Tinto
    "US3682872078", # Gazprom PAO 
    "US69343P1057", # NK Lukoil PAO
    "US88642R1095", # Tidewater Inc
    "LT0000128621", # Inter RAO Lietuva AB
    "US71654V4086", # ADR on Petróleo Brasileiro S.A.-Petrobras
    "IE00BM67HM91"  # Xtrackers MSCI World Energy UCITS ETF 1C
}

ENERGY_STOCK_SYMBOLS = {
    "EC", # Total Gabon
    "GAZ", # Gazprom
    "LKOD", # Lukoil
    "LUK.EUR", # Lukoil
    "SEPL", # Seplat energy plc
    "RIO", # RIO tinto plc
    "PKN", # Orlen SA
    "MAU", # Maurel & PROM
    "XDW0" # Xtrackers MSCI World Energy UCITS ETF 1C
}

def is_isin_energy_stock(isin: str) -> bool:
    """
    Check if the provided ISIN corresponds to an energy stock.

    Args:
        isin (str): The ISIN to check.

    Returns:
        bool: True if the ISIN is in the energy stock list, False otherwise.
    """
    return isin in ENERGY_STOCK_ISINS

def is_symbol_energy_stock(symbol: str) -> bool:
    """
    Check if the provided symbol corresponds to an energy stock.

    Args:
        symbol (str): The symbol to check.

    Returns:
        bool: True if the symbol is in the energy stock list, False otherwise.
    """
    return symbol in ENERGY_STOCK_SYMBOLS
