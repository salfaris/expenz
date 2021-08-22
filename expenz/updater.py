from datetime import datetime
from typing import TypeVar
import numpy as np
import pandas as pd
from helpers import ema_single

DataFrame = TypeVar('pandas.core.frame.DataFrame')

TODAY = datetime.today()

def append_row_by_date(df: DataFrame, path: str, for_date: datetime):
    df = df.reset_index()
    
    idx_to_insert_at = np.searchsorted(
        df.date,
        for_date,
    )
    
    df_as_array = df.values
    
    prev_row_data = df_as_array[idx_to_insert_at-1].tolist()
    prev_row_ema = prev_row_data[3]
    
    df_as_array = np.insert(
        df_as_array,
        idx_to_insert_at,
        np.array(get_row_data_from_user(
            for_date=for_date, prev_row_ema=prev_row_ema)),
        axis=0
    )
    
    df = pd.DataFrame(df_as_array, columns=df.columns)
    
    df.set_index('date', inplace=True)
    df.to_csv(path, date_format='%Y-%m-%d')

def update_row(df: DataFrame, path: str):
    df = df.reset_index()
    
    last_row_data = df.values[-1].tolist()
    last_row_date = last_row_data[0]
    last_row_ema = last_row_data[3]

    # Only update if still the same month, else append.
    if last_row_date.month == TODAY.month:
        df = df[:-1]

    df.loc[len(df)] = get_row_data_from_user(
        for_date=TODAY, prev_row_ema=last_row_ema)

    df.set_index('date', inplace=True)
    df.to_csv(path, date_format='%Y-%m-%d')
    
def get_row_data_from_user(for_date: datetime, prev_row_ema: float):
    print("Total money spent in {}?"\
            .format(for_date.strftime("%B %Y")))

    while True:
        try:
            amount = float(input())
            break
        except ValueError:
            print("Please insert float value only. Example: 95.52")
        except TypeError:
            print("Please insert float value only. Example: 95.52")

    cost_per_person = float(amount) / 5
    
    row_data = [
        pd.Timestamp(for_date.replace(day=1)),
        amount,
        cost_per_person,
        ema_single(price=cost_per_person, span=3, prev_ema=prev_row_ema),
    ]
    
    return row_data

def recalculate_ema(df: DataFrame, path: str):
    df = df.reset_index()
    
    new_ema = []

    prev_ema = 0.
    for idx, row in df.iterrows():
        if idx == 0:
            new_ema.append(row.cost_per_person)
            prev_ema = row.cost_per_person
            continue
        prev_ema = ema_single(
            price=row.cost_per_person,
            span=3,
            prev_ema=prev_ema
        )
        new_ema.append(prev_ema)
        
    df['ema_three'] = new_ema
    
    df.set_index('date', inplace=True)
    df.to_csv(path, date_format='%Y-%m-%d')