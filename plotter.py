# Local import
from helpers import gbp, get_now_month_year

# Third-party imports
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

plt.style.use('seaborn')

def save_get_plot(df: pd.DataFrame, path: str) -> None:
    data = {
        "title": ("95 Princess Court Groceries (Sep. 2019 /"
                  + f" {get_now_month_year()})"),
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