import numpy as np
import matplotlib.pyplot as plt

def AMDnLockboxes_process(AMDnLockboxes, market, client):
    nscen, nyrs = market['cumRmsM'].shape
    n = AMDnLockboxes['cumRmDistributionYear']
    n = max(n, 2)
    n = min(n, nyrs)

    xfs = np.zeros(n - 1)
    xms = np.ones(n - 1)
    xs = np.vstack([xfs, xms])

    for yr in range(n, nyrs + 1):
        x = np.sort(market['cumRmsM'][:, yr - 1])
        y = np.sort(market['cumRmsM'][:, n - 1])
        xvals = np.column_stack([np.ones(len(x)), x])
        b, _, _, _ = np.linalg.lstsq(xvals, y, rcond=None)
        xf = b[0] / np.mean(market['cumRfsM'][:, yr - 1])
        xm = b[1]
        xs = np.hstack([xs, [[xf], [xm]]])

    AMDnLockboxes['proportions'] = xs

    if AMDnLockboxes['showProportions'].lower() == 'y':
        fig, ax = plt.subplots()
        x = np.arange(1, xs.shape[1] + 1)
        ax.bar(x, xs[0, :], label='TIPS')
        ax.bar(x, xs[1, :], bottom=xs[0, :], label='Market')
        ax.grid(True)
        ax.set_xlabel('Lockbox Maturity Year')
        ax.set_ylabel('Amount Invested at Inception')
        ax.legend(['TIPS', 'Market'])
        ax.set_xlim([0, nyrs + 1])
        title = f'Lockbox Contents for Approximating Market Distribution in year {n}'
        ax.set_title(title, color='b')
        plt.show()

    return AMDnLockboxes
