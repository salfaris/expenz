# Local and system imports
from helpers import gbp, get_now_month_year
import os
from PIL import Image
from sys import argv, exit
from datetime import datetime

# Third-party imports
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
plt.style.use('seaborn')

def main():
    df = pd.read_csv('data/95pc_new.csv',
                    header=0,
                    index_col=0,
                    parse_dates=True,
                    infer_datetime_format=True)

    chart_name = datetime.today().strftime("%b%y") + "chart"
    
    target_dir = 'charts'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    target_path = os.path.join(target_dir, chart_name + ".png")
    save_get_plot(df, target_path)
    Image.open(target_path).show()

def save_get_plot(df: pd.DataFrame, path: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df.index,
            df.cost_per_person,
            marker='o',
            label="Cost/person (£)",
            color='green')

    ax.plot(df.index,
            df.ema_three,
            label="EMA (3 months)",
            linestyle='dashed',
            color='orange',
            alpha=0.7)

    ax.set(title=f"95 Princess Court Groceries (Sep. 2019 / {get_now_month_year()})",
        xlabel="Month",
        ylabel="Cost (£)")

    date_form = DateFormatter("%b. %y")
    ax.xaxis.set_major_formatter(date_form)

    for x, y in zip(df.index.to_list(), df.cost_per_person.to_list()):

        plt.annotate(gbp(y), (x,y),
                    textcoords='offset points',
                    xytext=(5, -15),
                    ha='center')

    plt.xticks(rotation=0)
    plt.legend()
    fig.savefig(path, bbox_inches='tight')
    
if __name__ == '__main__':
    main()