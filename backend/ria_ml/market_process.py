import numpy as np

def market_process(market, client):
    nrows, ncols = client['pStatesM'].shape

    u = market['eC']
    v = market['sdC']**2
    b = np.sqrt(np.log(v / u**2 + 1))
    a = 0.5 * np.log(u**2 / np.exp(b**2))
    market['csM'] = np.exp(a + b * np.random.randn(nrows, ncols))
    m = np.cumprod(market['csM'], axis=1)
    market['cumCsM'] = np.hstack([np.ones((nrows, 1)), m[:, :-1]])

    market['rfsM'] = market['rf'] * np.ones((nrows, ncols))
    m = np.cumprod(market['rfsM'], axis=1)
    market['cumRfsM'] = np.hstack([np.ones((nrows, 1)), m[:, :-1]])

    u = market['exRm'] + (market['rf'] - 1)
    v = market['sdRm']**2
    b = np.sqrt(np.log(v / u**2 + 1))
    a = 0.5 * np.log(u**2 / np.exp(b**2))
    market['rmsM'] = np.exp(a + b * np.random.randn(nrows, ncols))
    m = np.cumprod(market['rmsM'], axis=1)
    market['cumRmsM'] = np.hstack([np.ones((nrows, 1)), m[:, :-1]])

    b = np.log(u / market['rf']) / np.log(1 + market['sdRm']**2 / u**2)
    a = np.sqrt(u * market['rf'])**(b - 1)
    as_ = np.ones((nrows, 1)) * (a**np.arange(ncols))
    market['ppcsM'] = as_ * (market['cumRmsM']**(-b))
    market['pvsM'] = market['ppcsM'] / nrows
    market['avec'] = as_[0, :]
    market['b'] = b

    return market
