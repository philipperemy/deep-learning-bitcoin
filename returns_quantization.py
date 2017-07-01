import sys

import pandas as pd

from data_manager import file_processor
from utils import compute_returns


def generate(data_folder, bitcoin_file):
    p = file_processor(bitcoin_file)
    close_prices_returns = compute_returns(p)
    num_bins = 10
    returns_bins = pd.cut(close_prices_returns, num_bins).values.categories
    returns_labels = pd.cut(close_prices_returns, num_bins, labels=False)
    print(returns_bins)
    print(returns_labels)


def main():
    arg = sys.argv
    assert len(arg) == 3, 'Usage: python3 {} DATA_FOLDER_TO_STORE_GENERATED_DATASET ' \
                          'BITCOIN_MARKET_DATA_CSV_PATH'.format(arg[0])
    data_folder = arg[1]
    bitcoin_file = arg[2]
    generate(data_folder, bitcoin_file)


if __name__ == '__main__':
    main()
