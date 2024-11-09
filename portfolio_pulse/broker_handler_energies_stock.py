ENERGY_STOCK_ISINS = {
    "GA0000121459", # Total Gabon
    "FR0000051070", # Maurel & Prom 
    "JE00B55Q3P39", # Genel Energy PLC
    "GB0007188757", # Rio Tinto
    "US3682872078", # Gazprom PAO 
    "US69343P1057", # NK Lukoil PAO
    "US88642R1095", # Tidewater Inc
    "LT0000128621", # Inter RAO Lietuva AB
    "US71654V4086", # ADR on Petróleo Brasileiro S.A.-Petrobras
}

def is_energy_stock(isin: str) -> bool:
    """
    Check if the provided ISIN corresponds to an energy stock.

    Args:
        isin (str): The ISIN to check.

    Returns:
        bool: True if the ISIN is in the energy stock list, False otherwise.
    """
    return isin in ENERGY_STOCK_ISINS
