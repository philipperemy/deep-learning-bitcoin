import os
import shutil
import sys
from time import time
from uuid import uuid4

import numpy as np

from data_manager import file_processor
from returns_quantization import add_returns_in_place
from utils import *


def generate_quantiles(data_folder, bitcoin_file):
    btc_df = file_processor(bitcoin_file)
    btc_df, levels = add_returns_in_place(btc_df)

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

        predict_label = str(btc_df[i + slice_size:i + slice_size + 1]['close_prices_returns_labels'].values[0])

        save_dir = os.path.join(data_folder, 'train', predict_label)
        if epoch % test_every_steps == 0:
            save_dir = os.path.join(data_folder, 'test', predict_label)
        mkdir_p(save_dir)
        save_to_file(btc_slice, filename=save_dir + '/' + str(uuid4()) + '.png')

        print('epoch = {0}, time = {1:.3f}'.format(str(epoch).zfill(8), time() - st))


def generate_up_down(data_folder, bitcoin_file):
    p = file_processor(bitcoin_file)
    slice_size = 40
    test_every_steps = 10
    n = len(p) - slice_size

    shutil.rmtree(data_folder, ignore_errors=True)
    for epoch in range(int(1e6)):
        st = time()

        i = np.random.choice(n)
        sl = p[i:i + slice_size]

        if sl.isnull().values.any():
            # sometimes prices are discontinuous and nothing happened in one 5min bucket.
            # in that case, we consider this slice as wrong and we ask for a new one.
            # it's likely to happen at the beginning of the data set where the volumes are low.
            continue

        last_price = sl[-2:-1]['price_close'].values[0]
        next_price = p[i + slice_size:i + slice_size + 1]['price_close'].values[0]

        if last_price < next_price:
            direction = 'UP'
        else:
            direction = 'DOWN'

        save_dir = os.path.join(data_folder, 'train', direction)
        if epoch % test_every_steps == 0:
            save_dir = os.path.join(data_folder, 'test', direction)
        mkdir_p(save_dir)
        save_to_file(sl, filename=save_dir + '/' + str(uuid4()) + '.png')

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
