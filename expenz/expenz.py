# Local and system imports
import updater
from visuals import save_get_plot
import os
from PIL import Image
from sys import argv, exit
from datetime import datetime
from dateutil.parser import parse

# Third-party imports
import pandas as pd

FILEPATH = 'data/95pc_new_copy.csv'
CHARTPATH = 'charts'

def main():
    df = pd.read_csv(FILEPATH,
                    header=0,
                    index_col=0,
                    parse_dates=True,
                    infer_datetime_format=True)

    if len(argv) > 2:
        print("Usage: python groceries.py [ -r | -u | -p ]")
        exit(1)
    
    elif len(argv) == 1 or argv[1] == '-r':
        print(df.reset_index())
        exit(0)
    
    elif argv[1] == '--add':
        print("Date to add: ")
        
        while True:
            try:
                add_date = parse(input())
                break
            except ValueError:
                print("Invalid date. Example: 2020 August 21")
            except TypeError:
                print("Invalid date. Example: 2020 August 21")
        
        updater.append_row_by_date(df, FILEPATH, for_date=add_date)
        exit(0)
    
    elif argv[1] == '-u':
        updater.update_row(df, FILEPATH)
        exit(0)
    
    elif argv[1] == '-p':
        plot_df(df)
        exit(0)
        
    elif argv[1] == '-up':
        updater.update_row(df, FILEPATH)
        plot_df(df)
        exit(0)


def plot_df(df: pd.DataFrame) -> None:
    # Name of chart when saving
    chart_name = datetime.today().strftime("%b%y") + "chart"
    
    # Create directory if not exists
    if not os.path.exists(CHARTPATH):
        os.makedirs(CHARTPATH)
    
    # Final path to save to
    target_path = os.path.join(CHARTPATH, chart_name + ".png")
    
    save_get_plot(df, target_path)
    Image.open(target_path).show()
    exit(0)
    
if __name__ == '__main__':
    main()