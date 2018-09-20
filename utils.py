import datetime

import matplotlib
import pandas as pd

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc


def compute_returns(p):
    close_prices = p['price_close']
    close_prices_returns = 100 * ((close_prices.shift(-1) - close_prices) / close_prices).fillna(0.0)
    return close_prices_returns.shift(1).fillna(0)


def prepare_plot(df):
    fig, ax = plt.subplots()
    candlestick2_ohlc(ax,
                      df['price_open'].values,
                      df['price_high'].values,
                      df['price_low'].values,
                      df['price_close'].values,
                      width=0.6,
                      colorup='g',
                      colordown='r',
                      alpha=1)
    plt.grid(True)
    return fig


def plot_p(df):
    prepare_plot(df)
    plt.show()


def save_to_file(df, filename):
    fig = prepare_plot(df)
    plt.savefig(filename)
    plt.close(fig)


def mkdir_p(path):
    import os
    import errno
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def raw_read(data_file):
    print('Reading bitcoin market data file: {}.'.format(data_file))
    d = pd.read_table(data_file, sep=',', header=None, index_col=0, names=['price', 'volume'])
    d.index = d.index.map(lambda ts: datetime.datetime.fromtimestamp(int(ts)))
    d.index.names = ['DateTime_UTC']
    return d


def file_processor(data_file, resample_frequency='1H'):
    d = raw_read(data_file)
    p = pd.DataFrame(d['price'].resample(resample_frequency).ohlc())
    p.columns = ['price_open', 'price_high', 'price_low', 'price_close']
    v = pd.DataFrame(d['volume'].resample(resample_frequency).sum())
    v.columns = ['volume']
    p['volume'] = v['volume']

    # drop NaN values.
    # for example sometimes we don't have data for like one hour in a row.
    # So we have NaN buckets of resample_frequency in this particular hour.
    # Our convention is to avoid those NaN values and drop them!
    p.dropna(inplace=True)
    # p.to_csv('/tmp/bitcoin_coinbase_{}.csv'.format(resample_frequency), sep='\t')
    return p


def count_ticks_per_day(data_file):
    d = raw_read(data_file)
    print('date, tick_count')
    for d_day in to_days(d):
        print('{}, {}'.format(str(d_day.index[0]).split(' ')[0], len(d_day)))


def to_days(df):
    return [g[1] for g in df.groupby([df.index.year, df.index.month, df.index.day])]  # DataFrame to List<Day>
