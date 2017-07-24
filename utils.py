def compute_returns(p):
    close_prices = p['price_close']
    close_prices_returns = 100 * ((close_prices.shift(-1) - close_prices) / close_prices).fillna(0.0)
    return close_prices_returns.shift(1).fillna(0)


def plot_p(df):
    import matplotlib.pyplot as plt
    from matplotlib.finance import candlestick2_ohlc
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
    plt.show()
    print('Done.')


def save_to_file(df, filename):
    import matplotlib.pyplot as plt
    from matplotlib.finance import candlestick2_ohlc
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
