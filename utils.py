import matplotlib

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
