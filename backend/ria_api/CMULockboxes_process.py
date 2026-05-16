import numpy as np
import matplotlib.pyplot as plt

def CMULockboxes_process(CMULockboxes, market, client):
    # computes lockbox proportions for an CMULockbox strategy

    # get number of years
    nyrs = market['cumRmsM'].shape[1]

    # set proportions for year 1
    mktprop = CMULockboxes['initialMarketProportion']
    if mktprop > 1: mktprop = 1
    if mktprop < 0: mktprop = 0
    tipsprop = 1 - mktprop

    # find ratio of market proportion each year to that for the prior year
    a = market['avec'][1]
    b = market['b']
    logk = (-np.log(1/a)) / b
    k = np.exp(logk)

    # compute market proportions for all years
    mktprops = mktprop * (1/k)**np.arange(nyrs)

    # compute TIPS proportions for all years
    tipsprops = tipsprop * (1/market['rf'])**np.arange(nyrs)

    # compute lockbox proportions
    CMULockboxes['proportions'] = np.vstack((tipsprops, mktprops))

    # plot contents if requested
    if CMULockboxes['showProportions'].lower() == 'y':
        xs = CMULockboxes['proportions']
        fig, ax = plt.subplots()
        x = np.arange(1, nyrs + 1)
        ax.bar(x, xs.T, label=['TIPS', 'Market'])
        ax.grid(True)
        ax.set_fontsize(30)
        ss = client['figurePosition']
        fig.set_size_inches(ss[2], ss[3])
        fig.patch.set_facecolor('white')
        ax.set_xlabel('Lockbox Maturity Year', fontsize=30)
        ax.set_ylabel('Amount Invested at Inception', fontsize=30)
        ax.legend()
        ax.set_xlim([0, nyrs + 1])
        ax.set_ylim([0, 1])
        t = 'Lockbox Proportions for Constant Marginal Utility'
        ax.set_title(t, fontsize=40, color='b')
        plt.show()
