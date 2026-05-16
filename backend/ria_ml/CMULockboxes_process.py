import numpy as np
import matplotlib.pyplot as plt

def CMULockboxes_process(CMULockboxes, market, client):
    nscen, nyrs = market['cumRmsM'].shape

    mktprop = np.clip(CMULockboxes['initialMarketProportion'], 0, 1)
    tipsprop = 1 - mktprop

    a = market['avec'][1]
    b = market['b']
    logk = -np.log(1 / a) / b
    k = np.exp(logk)
    mktprops = mktprop * ((1 / k)**np.arange(nyrs))
    tipsprops = tipsprop * ((1 / market['rf'])**np.arange(nyrs))

    CMULockboxes['proportions'] = np.vstack([tipsprops, mktprops])

    if CMULockboxes['showProportions'].lower() == 'y':
        xs = CMULockboxes['proportions']
        fig, ax = plt.subplots()
        x = np.arange(1, xs.shape[1] + 1)
        ax.bar(x, xs[0, :], label='TIPS')
        ax.bar(x, xs[1, :], bottom=xs[0, :], label='Market')
        ax.grid(True)
        ax.set_xlabel('Lockbox Maturity Year')
        ax.set_ylabel('Amount Invested at Inception')
        ax.legend(['TIPS', 'Market'])
        ax.set_xlim([0, nyrs + 1])
        ax.set_title('Lockbox Proportions for Constant Marginal Utility', color='b')
        plt.show()

    return CMULockboxes
