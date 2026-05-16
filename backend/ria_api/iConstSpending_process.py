import numpy as np

def iConstSpending_process(iConstSpending, client, market):
    # get matrix dimensions
    nscen, nyrs = market.rmsM.shape
    
    # get glidepath
    path = iConstSpending.glidePath
 
    # get points from glidepath
    ys = path[0, :]
    xs = path[1, :]
    # insure no years prior to 1
    xs = np.maximum(xs, 1)
    # insure no market proportions greater than 1 or less than 0
    ys = np.minimum(ys, 1)
    ys = np.maximum(ys, 0)
    # sort points in increasing order of x values
    sorted_indices = np.argsort(xs)
    xs = xs[sorted_indices]
    ys = ys[sorted_indices]
    # add values for year 1 and/or last year if needed
    if xs[0] > 1:
        xs = np.concatenate(([1], xs))
        ys = np.concatenate(([ys[0]], ys))
    if xs[-1] < nyrs:
        xs = np.concatenate((xs, [nyrs]))
        ys = np.concatenate((ys, [ys[-1]]))

    # Create vectors for all years
    pathxs = []
    pathys = []

    for i in range(len(xs) - 1):
        xlft = xs[i]
        xrt = xs[i + 1]
        ylft = ys[i]
        yrt = ys[i + 1]

        pathxs.append(xlft)
        pathys.append(ylft)

        if xlft != xrt:
            slope = (yrt - ylft) / (xrt - xlft)
            for x in range(xlft + 1, xrt):
                pathxs.append(x)
                yy = ylft + slope * (x - xlft)
                pathys.append(yy)

    pathxs.append(xs[-1])
    pathys.append(ys[-1])

	
    # show glide path if desired
    if iConstSpending.showGlidePath.lower() == 'y':
        fig = plt.figure()
        plt.rcParams.update({'font.size': 30})
        fig.patch.set_facecolor([1, 1, 1])
        plt.xlabel('Year', fontsize=30)
        plt.ylabel('Proportion in Market Portfolio', fontsize=30)
        plt.plot(path[1, :], path[0, :], '*b', linewidth=4)
        plt.plot(xs, ys, '-r', linewidth=2)
        plt.legend(['Input', 'All'])
        plt.axis([0, nyrs + 1, 0, 1])
        plt.title('Glide Path: Market Proportions by Year', fontsize=40, color='b')
        plt.grid()
        plt.show()
    
    # create matrix of gross returns for investment strategy
    retsM = np.zeros((nscen, nyrs))
    for yr in range(nyrs - 1):
        rets = pathys[yr] * market.rmsM[:, yr]
        rets = rets + (1 - pathys[yr]) * market.rfsM[:, yr]
        retsM[:, yr] = rets
    
    # get retention ratio
    rr = iConstSpending.retentionRatio
    
    # create vector of initial portfolio values
    portvals = np.ones((nscen, 1)) * iConstSpending.investedAmount
    
    # initialize desired spending matrix
    desiredSpendingM = np.zeros((nscen, nyrs))
    
    # create matrix of desired real spending for highest personal state
    prop = iConstSpending.initialProportionSpent
    amt = prop * iConstSpending.investedAmount
    gradRatio = iConstSpending.graduationRatio
    factors = gradRatio ** np.arange(nyrs)
    maxSpendingM = np.ones((nscen, 1)) * (amt * factors)
    
    # add amounts to desired spending matrix
    props = iConstSpending.pStateRelativeIncomes
    props = props / max(props)
    props = np.maximum(props, 0)
    for ps in range(1, 4):
        s = maxSpendingM * props[ps - 1]
        m = (client.pStatesM == ps) * s
        desiredSpendingM += m
    
    # initialize incomes and fees matrices
    incsM = np.zeros((nscen, nyrs))
    feesM = np.zeros((nscen, nyrs))
    
    # compute incomes paid at the beginning of year 1
    incsM[:, 0] = np.minimum(desiredSpendingM[:, 0], portvals[:, 0])
    
    # compute portfolio values after income payments
    portvals = portvals - incsM[:, 0]
    
    # compute incomes and fees paid at beginning of each subsequent year
    for yr in range(1, nyrs):
        # compute portfolio values before deductions
        portvals = portvals * retsM[:, yr - 1]
        
        # compute and deduct fees paid at beginning of year
        feesV = (1 - rr) * portvals
        feesM[:, yr] = feesV
        portvals = portvals - feesV
        
        # compute incomes paid out at beginning of year in states 1,2 or 3
        v = (client.pStatesM[:, yr] > 0) & (client.pStatesM[:, yr] < 4)
        incsM[:, yr] = v * np.minimum(desiredSpendingM[:, yr], portvals)
        
        # pay entire value if state 4
        v = (client.pStatesM[:, yr] == 4)
        incsM[:, yr] += v * portvals
        
        # deduct incomes paid from portfolio values
        portvals = portvals - incsM[:, yr]
    
    # add incomes and fees to client matrices
    client.incomesM += incsM
    client.feesM += feesM
    
    return client