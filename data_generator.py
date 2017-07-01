import os
import shutil
from time import time
from uuid import uuid4

import numpy as np

from data_manager import file_processor
from utils import *

DATA_FOLDER = '/tmp/btc-trading-patterns/'


def generate():
    p = file_processor()
    slice_size = 40
    test_every_steps = 10
    n = len(p) - slice_size

    shutil.rmtree(DATA_FOLDER, ignore_errors=True)
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

        save_dir = os.path.join(DATA_FOLDER, 'train', direction)
        if epoch % test_every_steps == 0:
            save_dir = os.path.join(DATA_FOLDER, 'test', direction)
        mkdir_p(save_dir)
        save_to_file(sl, filename=save_dir + '/' + str(uuid4()) + '.png')

        print('epoch = {0}, time = {1:.3f}'.format(str(epoch).zfill(8), time() - st))


if __name__ == '__main__':
    generate()
