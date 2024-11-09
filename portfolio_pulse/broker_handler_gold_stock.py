GOLD_STOCK_ISINS = {
    "DE000A0S9GB0", # Deutsche Boerse Commodities Xetra-Gold ETC
    "AU000000GRR8", # Grange Resources Ltd
    "CA32076V1031", # First Majestic Silver Corp
    "AU0000221418", # Ten Sixty Four Ltd
    "CH0047533523", # ZKB Gold ETF AA EUR
    "CA3499421020", # FORTUNA SILVER MINES INC ORDINARY SHARES (CANADA)
    "CA0679011084", # Barrick Gold Corp
    "CH0183136057", # ZKB Platinum ETF AA CHF
    "US4132163001", # ADR on Harmony Gold Mining Company Ltd
}

def is_gold_stock(isin: str) -> bool:
    """
    Check if the provided ISIN corresponds to an energy stock.

    Args:
        isin (str): The ISIN to check.

    Returns:
        bool: True if the ISIN is in the energy stock list, False otherwise.
    """
    return isin in GOLD_STOCK_ISINS
