from helpers import ema_single
from datetime import datetime
import os
import csv

import pandas as pd

TODAY = datetime.today()

def update_row(df: pd.DataFrame, path: str):
    df = df.reset_index()
    
    last_row_data = df.values[-1].tolist()
    last_row_date = last_row_data[0]
    last_row_ema = last_row_data[3]

    # Only update if still the same month, else append.
    if last_row_date.month == TODAY.month:
        df = df[:-1]

    print("Total money spent in {}?"\
            .format(TODAY.strftime("%B %Y")))

    amount = float(input())
    cost_per_person = float(amount) / 5

    to_update = [
            TODAY.replace(day=1),
            amount,
            cost_per_person,
            ema_single(cost_per_person, 3, last_row_ema),
    ]

    df.loc[len(df)] = to_update

    df.set_index('date', inplace=True)
    df.to_csv(path, date_format='%Y-%m-%d')