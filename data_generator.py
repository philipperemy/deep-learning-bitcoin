import os
import shutil
import sys
from time import time
from uuid import uuid4

import numpy as np

from data_manager import file_processor
from utils import *


def generate(data_folder, bitcoin_file):
    p = file_processor(bitcoin_file)
    slice_size = 40
    test_every_steps = 10
    n = len(p) - slice_size

    shutil.rmtree(data_folder, ignore_errors=True)
    for epoch in range(int(1e5)):
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
    generate(data_folder, bitcoin_file)


if __name__ == '__main__':
    main()
