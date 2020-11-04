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
    """Returns the month year format of a datetime object."""
    return dt.strftime("%b %Y")

def get_now_month_year() -> str:
    return get_month_year(datetime.today())

def ema_single(price: float, span: int, prev_ema: float) -> float:
    """Returns a single EMA value."""
    factor = 2 / float(span+1)
    return (price-prev_ema)*factor + prev_ema