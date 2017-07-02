import os
import shutil
import sys
from time import time
from uuid import uuid4

import numpy as np

from data_manager import file_processor
from utils import *


def generate_quantiles(data_folder, bitcoin_file):
    def get_label(btc_df, btc_slice, i, slice_size):
        class_name = str(btc_df[i + slice_size:i + slice_size + 1]['close_prices_returns_labels'].values[0])
        return class_name

    return generate_cnn_dataset(data_folder, bitcoin_file, get_label)


def generate_up_down(data_folder, bitcoin_file):
    def get_price_direction(btc_df, btc_slice, i, slice_size):
        last_price = btc_slice[-2:-1]['price_close'].values[0]
        next_price = btc_df[i + slice_size:i + slice_size + 1]['price_close'].values[0]
        if last_price < next_price:
            class_name = 'UP'
        else:
            class_name = 'DOWN'
        return class_name

    return generate_cnn_dataset(data_folder, bitcoin_file, get_price_direction)


def generate_cnn_dataset(data_folder, bitcoin_file, get_class_name):
    btc_df = file_processor(bitcoin_file)
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
            # in that case, we consider this slice as wrong and we ask for a new one.
            # it's likely to happen at the beginning of the data set where the volumes are low.
            continue

        class_name = get_class_name(btc_df, btc_slice, i, slice_size)
        save_dir = os.path.join(data_folder, 'train', class_name)
        if epoch % test_every_steps == 0:
            save_dir = os.path.join(data_folder, 'test', class_name)
        mkdir_p(save_dir)
        save_to_file(btc_slice, filename=save_dir + '/' + str(uuid4()) + '.png')
        print('epoch = {0}, time = {1:.3f}'.format(str(epoch).zfill(8), time() - st))


def main():
    arg = sys.argv
    assert len(arg) == 3, 'Usage: python3 {} DATA_FOLDER_TO_STORE_GENERATED_DATASET ' \
                          'BITCOIN_MARKET_DATA_CSV_PATH'.format(arg[0])
    data_folder = arg[1]
    bitcoin_file = arg[2]
    generate_quantiles(data_folder, bitcoin_file)


if __name__ == '__main__':
    main()
