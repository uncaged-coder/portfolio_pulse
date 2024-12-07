GOLD_STOCK_ISINS = {
    "DE000A0S9GB0", # Deutsche Boerse Commodities Xetra-Gold ETC
    #"AU000000GRR8", # Grange Resources Ltd
    #"CA32076V1031", # First Majestic Silver Corp
    #"AU0000221418", # Ten Sixty Four Ltd
    "CH0047533523", # ZKB Gold ETF AA EUR
    #"CA3499421020", # FORTUNA SILVER MINES INC ORDINARY SHARES (CANADA)
    #"CA0679011084", # Barrick Gold Corp
    "CH0183136057", # ZKB Platinum ETF AA CHF
    #"US4132163001", # ADR on Harmony Gold Mining Company Ltd
}

GOLD_STOCK_SYMBOLS = {
    #"HMY", # harmony gold
    #"ECOR", # Ecora ressources PLC (colbat, charbon a coke, fer, cuivre, vanadium, uranium, OR
    #"GOLD",
    #"GLDG",
    #"FMV",
    #"FSM",
    "ZSILEU",
    "ZGLDEU",
    #"4GLD",
    #"MOGO", # X64
    #"GRR" # grange ressources
}

def is_isin_gold_stock(isin: str) -> bool:
    """
    Check if the provided ISIN corresponds to an gold stock.

    Args:
        isin (str): The ISIN to check.

    Returns:
        bool: True if the ISIN is in the gold stock list, False otherwise.
    """
    return isin in GOLD_STOCK_ISINS

def is_symbol_gold_stock(symbol: str) -> bool:
    """
    Check if the provided symbol corresponds to an gold stock.

    Args:
        symbol (str): The ISIN to check.

    Returns:
        bool: True if the symbol is in the gold stock list, False otherwise.
    """
    return symbol in GOLD_STOCK_SYMBOLS
