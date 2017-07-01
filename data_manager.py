import datetime

import pandas as pd

from utils import save_to_file

DATA_FILE = '/tmp/coinbaseUSD_mini.csv'


# http://api.bitcoincharts.com/v1/csv/

def file_processor():
    print('Reading.')
    d = pd.read_table(DATA_FILE, sep=',', header=None, index_col=0, names=['price', 'volume'])
    d.index = d.index.map(lambda ts: datetime.datetime.fromtimestamp(int(ts)))
    d.index.names = ['DateTime_UTC']
    p = pd.DataFrame(d['price'].resample('5Min').ohlc())
    p.columns = ['price_open', 'price_high', 'price_low', 'price_close']
    v = pd.DataFrame(d['volume'].resample('5Min').sum())
    v.columns = ['volume']
    p['volume'] = v['volume']
    p.to_csv('/tmp/bitcoin_coinbase_M5.csv', sep='\t')
    return p


if __name__ == '__main__':
    p = file_processor()
    save_to_file(p, '1.png')
    save_to_file(p, '2.png')
