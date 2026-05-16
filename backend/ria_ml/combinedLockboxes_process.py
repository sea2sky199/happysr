import numpy as np
import matplotlib.pyplot as plt

def combinedLockboxes_process(combinedLockboxes, client):
    wts = np.array(combinedLockboxes['componentWeights'], dtype=float)
    wts = np.maximum(wts, 0)
    wts = wts / np.sum(wts)

    boxprops = np.array(combinedLockboxes['componentLockboxes'][0]['proportions'])
    combprops = wts[0] * boxprops
    for i in range(1, len(combinedLockboxes['componentLockboxes'])):
        boxprops = np.array(combinedLockboxes['componentLockboxes'][i]['proportions'])
        combprops = combprops + wts[i] * boxprops
    combinedLockboxes['proportions'] = combprops

    xs = combprops
    nyrs = xs.shape[1]
    if combinedLockboxes['showCombinedProportions'].lower() == 'y':
        fig, ax = plt.subplots()
        x = np.arange(1, nyrs + 1)
        ax.bar(x, xs[0, :], label='TIPS')
        ax.bar(x, xs[1, :], bottom=xs[0, :], label='Market')
        ax.grid(True)
        ax.set_xlabel('Lockbox Maturity Year')
        ax.set_ylabel('Amount Invested at Inception')
        ax.legend(['TIPS', 'Market'])
        ax.set_xlim([0, nyrs + 1])
        ax.set_title(f"Lockbox Proportions for {combinedLockboxes['title']}", color='b')
        plt.show()

    return combinedLockboxes
