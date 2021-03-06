from helpers import ema_single
from datetime import datetime
from typing import TypeVar
import os

DataFrame = TypeVar('pandas.core.frame.DataFrame')

TODAY = datetime.today()

def update_row(df: DataFrame, path: str):
    df = df.reset_index()
    
    last_row_data = df.values[-1].tolist()
    last_row_date = last_row_data[0]
    last_row_ema = last_row_data[3]

    # Only update if still the same month, else append.
    if last_row_date.month == TODAY.month:
        df = df[:-1]

    print("Total money spent in {}?"\
            .format(TODAY.strftime("%B %Y")))

    while True:
        try:
            amount = float(input())
            break
        except ValueError:
            print("Please insert float value only. Example: 95.52")
        except TypeError:
            print("Please insert float value only. Example: 95.52")

    cost_per_person = float(amount) / 5
    
    to_update = [
            TODAY.replace(day=1),
            amount,
            cost_per_person,
            ema_single(price=cost_per_person, span=3, prev_ema=last_row_ema),
    ]

    df.loc[len(df)] = to_update

    df.set_index('date', inplace=True)
    df.to_csv(path, date_format='%Y-%m-%d')