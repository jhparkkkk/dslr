import sys
import pandas as pd

from src.Compute import Compute

def main():
    try:
        filename = sys.argv[1]
        dataset = pd.read_csv(filename, index_col=0)

        columns = dataset.dropna(axis=1, how='all').select_dtypes(include="number").columns.tolist()

        dataframe = pd.DataFrame(
            columns=columns,
            index=['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
        )

        for column in columns:
            values = dataset[column].tolist()
            dataframe[column]['Count'] = '{:9f}'.format(Compute.count(values))
            dataframe[column]['Mean'] = '{:9f}'.format(Compute.mean(values))
            dataframe[column]['Std'] = '{:9f}'.format(Compute.std(values))
            dataframe[column]['Min'] = '{:9f}'.format(Compute.min(values))
            dataframe[column]['25%'] = '{:9f}'.format(Compute.percentile(values, 25))
            dataframe[column]['50%'] = '{:9f}'.format(Compute.percentile(values, 50))
            dataframe[column]['75%'] = '{:9f}'.format(Compute.percentile(values, 75))
            dataframe[column]['Max'] = '{:9f}'.format(Compute.max(values))

        print(dataframe)

    except Exception as err:
        print(f'error: {err}')

if __name__ == "__main__":
    main()