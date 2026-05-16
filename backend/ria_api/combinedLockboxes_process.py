import numpy as np
import matplotlib.pyplot as plt

def combinedLockboxes_process(combinedLockboxes, client):
    n = len(combinedLockboxes['componentLockboxes'])
    wts = np.maximum(combinedLockboxes['componentWeights'], 0)
    wts = wts / np.sum(wts)
    
    boxprops = combinedLockboxes['componentLockboxes'][0]['proportions']
    combprops = wts[0] * boxprops
    for i in range(1, n):
        boxprops = combinedLockboxes['componentLockboxes'][i]['proportions']
        combprops = combprops + (wts[i] * boxprops)
    combinedLockboxes['proportions'] = combprops
    
    xs = combinedLockboxes['proportions']
    nyrs = xs.shape[1]
    if combinedLockboxes['showCombinedProportions'].lower() == 'y':
        fig = plt.figure()
        x = np.arange(1, nyrs+1)
        plt.bar(x, xs.T, stacked=True)
        plt.grid()
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.xlabel('Lockbox Maturity Year', fontsize=30)
        plt.ylabel('Amount Invested at Inception', fontsize=30)
        plt.legend(['TIPS', 'Market'])
        plt.axis([0, nyrs+1, 0, 1])
        plt.title(f"Lockbox Proportions for {combinedLockboxes['title']}", fontsize=40, color='b')
        plt.show()



