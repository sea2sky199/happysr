import numpy as np
import matplotlib.pyplot as plt

def AMDnLockboxes_process(AMDnLockboxes, market, client):
    # get number of years of returns
    nscen, nyrs = market.cumRmsM.shape
    
    # get n
    n = AMDnLockboxes.cumRmDistributionYear
    if n < 2:
        n = 2
    if n > nyrs:
        n = nyrs
    
    # set lockbox proportions for initial years to investment in the market portfolio
    xfs = np.zeros(n-1)
    xms = np.ones(n-1)
    xs = np.vstack((xfs, xms))
    
    # do regressions to compute contents of remaining lockboxes
    for yr in range(n, nyrs+1):
        # sort cumulative returns
        x = np.sort(market.cumRmsM[:, yr-1])
        y = np.sort(market.cumRmsM[:, n-1])
        
        # regress y values on x values
        xvals = np.column_stack((np.ones(len(x)), x))
        b = np.linalg.lstsq(xvals, y, rcond=None)[0]
        
        # compute lockbox contents
        xf = b[0] / np.mean(market.cumRfsM[:, yr-1])
        xm = b[1]
        
        # add to xs matrix
        xs = np.hstack((xs, np.array([xf, xm])))
    
    # add lockbox holdings to AMDnLockboxes
    AMDnLockboxes.proportions = xs
    
    # plot contents if requested
    if AMDnLockboxes.showProportions.lower() == 'y':
        fig = plt.figure()
        x = np.arange(1, xs.shape[1]+1)
        plt.bar(x, xs.T)
        plt.grid()
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.xlabel('Lockbox Maturity Year', fontsize=30)
        plt.ylabel('Amount Invested at Inception', fontsize=30)
        plt.legend(['TIPS', 'Market'])
        plt.axis([0, nyrs+1, 0, 1])
        plt.title(f'Lockbox Contents for Approximating Market Distribution in year {n}', fontsize=40, color='b')
        plt.show()
    
    return AMDnLockboxes