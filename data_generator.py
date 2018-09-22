import sys

import logging
import numpy as np
import os
import pandas as pd
import shutil
from tqdm import tqdm

from returns_quantization import add_returns_in_place
from utils import mkdir_p, save_to_file

logger = logging.getLogger(__name__)

np.set_printoptions(threshold=np.nan)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def generate_quantiles(data_folder, bitcoin_file):
    def get_label(btc_df, btc_slice, i, slice_size):
        class_name = str(btc_df[i + slice_size:i + slice_size + 1]['close_price_returns_labels'].values[0])
        return class_name

    return generate_cnn_dataset(data_folder, bitcoin_file, get_label)


def generate_up_down(data_folder, bitcoin_file):
    def get_price_direction(btc_df, btc_slice, i, slice_size):
        last_price = btc_slice[-1:]['price_close'].values[0]  # one option to get the correct last price
        # another option to get the correct last price
        # last_price = btc_df[i + slice_size - 1:i + slice_size]['price_close'].values[0]
        next_price = btc_df[i + slice_size:i + slice_size + 1]['price_close'].values[0]
        if last_price < next_price:
            class_name = 'UP'
        else:
            class_name = 'DOWN'
        return class_name

    return generate_cnn_dataset(data_folder, bitcoin_file, get_price_direction)


def dump_example_to_file(df, i, slice_size, get_class_name, data_folder, is_test):
    btc_slice = df[i:i + slice_size]
    if btc_slice.isnull().values.any():
        # sometimes prices are discontinuous and nothing happened in one 5min bucket.
        # in that case, we consider this slice as wrong and we raise an exception.
        # it's likely to happen at the beginning of the data set where the volumes are low.
        raise Exception('NaN values detected. Please remove them.')
    class_name = get_class_name(df, btc_slice, i, slice_size)
    save_dir = os.path.join(data_folder, 'test' if is_test else 'train', class_name)
    filename = os.path.join(save_dir, str(i)) + '.png'
    mkdir_p(save_dir)
    save_to_file(btc_slice, filename=filename)
    return filename


def generate_cnn_dataset(data_folder, bitcoin_file, get_class_name):
    btc_df = pd.read_csv(bitcoin_file)
    btc_df, levels = add_returns_in_place(btc_df)

    print('-' * 80)
    print('Those values should be roughly equal to 1/len(levels):')
    for ii in range(len(levels)):
        print(ii, np.mean((btc_df['close_price_returns_labels'] == ii).values))
    print(levels)
    print('-' * 80)

    shutil.rmtree(data_folder, ignore_errors=True)
    slice_size = 40
    cutoff = int(len(btc_df) * 0.9)
    btc_df_tr = btc_df[:cutoff]
    btc_df_te = btc_df[cutoff:]

    bar_train = tqdm(range(len(btc_df_tr) - slice_size - 1))
    for i in bar_train:
        filename = dump_example_to_file(btc_df_tr, i, slice_size, get_class_name, data_folder, is_test=False)
        bar_train.set_description(filename)
    bar_train.close()

    bar_test = tqdm(range(len(btc_df_te) - slice_size - 1))
    for i in bar_test:
        filename = dump_example_to_file(btc_df_te, i, slice_size, get_class_name, data_folder, is_test=True)
        bar_test.set_description(filename)
    bar_test.close()


def main():
    logging.basicConfig(format='%(asctime)12s - %(levelname)s - %(message)s', level=logging.INFO)
    args = sys.argv
    assert len(args) == 4, 'Usage: python3 {} DATA_FOLDER_TO_STORE_GENERATED_DATASET ' \
                           'BITCOIN_MARKET_DATA_CSV_PATH USE_QUANTILES'.format(args[0])
    data_folder = args[1]
    bitcoin_file = args[2]
    use_quantiles = int(args[3])

    data_gen_func = generate_quantiles if use_quantiles else generate_up_down
    print('Using: {}'.format(data_gen_func))
    data_gen_func(data_folder, bitcoin_file)


if __name__ == '__main__':
    main()
