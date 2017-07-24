import datetime

import pandas as pd


# http://api.bitcoincharts.com/v1/csv/

def file_processor(data_file):
    print('Reading bitcoin market data file here: {}.'.format(data_file))
    d = pd.read_table(data_file, sep=',', header=None, index_col=0, names=['price', 'volume'])
    d.index = d.index.map(lambda ts: datetime.datetime.fromtimestamp(int(ts)))
    d.index.names = ['DateTime_UTC']
    p = pd.DataFrame(d['price'].resample('5Min').ohlc())
    p.columns = ['price_open', 'price_high', 'price_low', 'price_close']
    v = pd.DataFrame(d['volume'].resample('5Min').sum())
    v.columns = ['volume']
    p['volume'] = v['volume']

    # drop NaN values.
    # for example sometimes we don't have data for like one hour in a row.
    # So we have NaN buckets of 5Min in this particular hour.
    # Our convention is to avoid those NaN values and drop them!
    p = p.dropna()
    p.to_csv('/tmp/bitcoin_coinbase_M5.csv', sep='\t')
    return p
