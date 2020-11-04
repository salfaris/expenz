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

    if len(argv) == 0 or '-r':
        print(df.reset_index())
        exit(0)
    
    # Name of chart when saving
    chart_name = datetime.today().strftime("%b%y") + "chart"
    
    # Name of directory to save into
    target_dir = 'charts'
    
    # Create directory if not exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Final path to save to
    target_path = os.path.join(target_dir, chart_name + ".png")
    
    save_get_plot(df, target_path)
    Image.open(target_path).show()

def save_get_plot(df: pd.DataFrame, path: str) -> None:
    data = {
        "title": f"95 Princess Court Groceries (Sep. 2019 / {get_now_month_year()})",
        "xlabel": "Month",
        "ylabel": "Cost (£)",
    }
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

    # Set the top ylimit to be the maximal y-value plus an offset of 10.
    ax.set_ylim(top=df.cost_per_person.max()+10)
    
    ax.set(title=data['title'], xlabel=data['xlabel'], ylabel=data['ylabel'])

    date_form = DateFormatter("%b. %y")
    ax.xaxis.set_major_formatter(date_form)

    for x, y in zip(df.index.to_list(), df.cost_per_person.to_list()):

        plt.annotate(gbp(y), (x,y),
                    textcoords='offset points',
                    xytext=(0, 10),
                    ha='center')

    plt.xticks(rotation=0)
    plt.legend()
    fig.savefig(path, bbox_inches='tight')
    
if __name__ == '__main__':
    main()