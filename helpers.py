from typing import List
from datetime import datetime

def gbp(str_gbp: str) -> str:
    """Returns a GBP formatted string.
    
    Example:
    >> gbp(3.141265)
    >> £3.14
    """
    return "£{:.2f}".format(str_gbp)


def get_month_year(dt: datetime) -> str:
    return dt.strftime("%b %Y")

def get_now_month_year() -> str:
    return get_month_year(datetime.today())

def ema(prices: List[float], span: int) -> List[float]:
    """Compute the EMA of a price list."""
    factor = 2 / float(span+1)
    ema_prices = [prices.pop(0)]
    for idx, price in enumerate(prices):
        current_ema = price*factor + ema_prices[idx]*(1-factor)
        ema_prices.append(current_ema)
    return ema_prices