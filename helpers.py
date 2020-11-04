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
    return get_month_year(datetime.todawy())