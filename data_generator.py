import os
import shutil
import sys
from time import time
from uuid import uuid4

import numpy as np
import pandas as pd

from data_manager import file_processor
from returns_quantization import add_returns_in_place
from utils import *

np.set_printoptions(threshold=np.nan)
pd.set_option('display.height', 1000)
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
        last_price = btc_slice[-2:-1]['price_close'].values[0] #this is actually the second last price
        last_price = btc_slice[-1:]['price_close'].values[0] #one option to get the correct last price
        last_price = btc_df[i + slice_size - 1:i + slice_size]['price_close'].values[0] #another option to get the correct last price

        next_price = btc_df[i + slice_size:i + slice_size + 1]['price_close'].values[0]
        if last_price < next_price:
            class_name = 'UP'
        else:
            class_name = 'DOWN'
        return class_name

    return generate_cnn_dataset(data_folder, bitcoin_file, get_price_direction)


def generate_cnn_dataset(data_folder, bitcoin_file, get_class_name):
    btc_df = file_processor(bitcoin_file)
    btc_df, levels = add_returns_in_place(btc_df)

    print('-' * 80)
    print('Those values should be roughly equal to 1/len(levels):')
    for ii in range(len(levels)):
        print(ii, np.mean((btc_df['close_price_returns_labels'] == ii).values))
    print(levels)
    print('-' * 80)

    slice_size = 40
    test_every_steps = 10
    n = len(btc_df) - slice_size

    shutil.rmtree(data_folder, ignore_errors=True)
    for epoch in range(int(1e6)):
        st = time()

        i = np.random.choice(n)
        btc_slice = btc_df[i:i + slice_size]

        if btc_slice.isnull().values.any():
            # sometimes prices are discontinuous and nothing happened in one 5min bucket.
            # in that case, we consider this slice as wrong and we raise an exception.
            # it's likely to happen at the beginning of the data set where the volumes are low.
            raise Exception('NaN values detected. Please remove them.')

        class_name = get_class_name(btc_df, btc_slice, i, slice_size)
        save_dir = os.path.join(data_folder, 'train', class_name)
        if epoch % test_every_steps == 0:
            save_dir = os.path.join(data_folder, 'test', class_name)
        mkdir_p(save_dir)
        filename = save_dir + '/' + str(uuid4()) + '.png'
        save_to_file(btc_slice, filename=filename)
        print('epoch = {0}, time = {1:.3f}, filename = {2}'.format(str(epoch).zfill(8), time() - st, filename))


def main():
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
