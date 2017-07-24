import sys

import pandas as pd

from data_manager import file_processor
from utils import compute_returns


def add_returns_in_place(df):  # modifies df
    close_prices_returns = compute_returns(df)
    num_bins = 10
    returns_bins = pd.qcut(close_prices_returns, num_bins)
    bins_categories = returns_bins.values.categories
    returns_labels = pd.qcut(close_prices_returns, num_bins, labels=False)

    df['close_price_returns'] = close_prices_returns
    df['close_price_returns_bins'] = returns_bins
    df['close_price_returns_labels'] = returns_labels

    return df, bins_categories


def generate_bins(bitcoin_file):
    p = file_processor(bitcoin_file)
    print(add_returns_in_place(p))


def main():
    arg = sys.argv
    assert len(arg) == 2, 'Usage: python3 {} BITCOIN_MARKET_DATA_CSV_PATH'.format(arg[0])
    bitcoin_file = arg[1]
    generate_bins(bitcoin_file)


if __name__ == '__main__':
    main()
