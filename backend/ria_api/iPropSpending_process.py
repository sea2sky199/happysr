import numpy as np
import matplotlib.pyplot as plt

def iPropSpending_process(iPropSpending, client, market):
    # get matrix dimensions
    nscen, nyrs = market['rmsM'].shape

    # get glidepath
    path = iPropSpending['glidePath']

    # get points from glidepath
    ys = path[0, :]
    xs = path[1, :]

    # ensure no years prior to 1
    xs = np.maximum(xs, 1)

    # ensure no market proportions greater than 1 or less than 0
    ys = np.minimum(ys, 1)
    ys = np.maximum(ys, 0)

    # sort points in increasing order of x values
    sorted_indices = np.argsort(xs)
    xs = xs[sorted_indices]
    ys = ys[sorted_indices]

    # add values for year 1 and/or last year if needed
    if xs[0] > 1:
        xs = np.insert(xs, 0, 1)
        ys = np.insert(ys, 0, ys[0])
    if xs[-1] < nyrs:
        xs = np.append(xs, nyrs)
        ys = np.append(ys, ys[-1])

    # create vectors for all years
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
    if iPropSpending['showGlidePath'].lower() == 'y':
        plt.figure(figsize=(10, 6))
        plt.xlabel('Year', fontsize=30)
        plt.ylabel('Proportion in Market Portfolio', fontsize=30)
        plt.plot(path[1, :], path[0, :], '*b', linewidth=4)
        plt.plot(xs, ys, '-r', linewidth=2)
        plt.legend(['Input', 'All'])
        plt.axis([0, nyrs + 1, 0, 1])
        plt.title('Glide Path: Market Proportions by Year', fontsize=40, color='b')
        plt.grid(True)
        plt.show()

    # create matrix of gross returns for investment strategy
    retsM = np.zeros((nscen, nyrs))
    for yr in range(nyrs - 1):
        rets = pathys[yr] * market['rmsM'][:, yr] + (1 - pathys[yr]) * market['rfsM'][:, yr]
        retsM[:, yr] = rets

    # get retention ratio
    rr = iPropSpending['retentionRatio']

    # get life expectancies
    if iPropSpending['useRMDlifeExpectancies'].lower() == 'y':
        LEs = [27.4, 26.5, 25.6, 24.7, 23.8, 22.9, 22.0, 21.2, 20.3, 19.5, 18.7, 17.9, 17.1,
               16.3, 15.5, 14.8, 14.1, 13.4, 12.7, 12.0, 11.4, 10.8, 10.2, 9.6, 9.1, 8.6,
               8.1, 7.6, 7.1, 6.7, 6.3, 5.9, 5.5, 5.2, 4.9, 4.5, 4.2, 3.9, 3.7, 3.4, 3.1,
               2.9, 2.6, 2.4, 2.1, 1.9]
        firstLEAge = 70
    else:
        LEs = iPropSpending['nonRMDlifeExpectancies']
        firstLEAge = iPropSpending['nonRMDfirstLEAge']

    # expand LE vector
    firstLE = LEs[0]
    initLEs = firstLE + np.arange(firstLEAge - 1, 0, -1)
    LEs = np.concatenate((initLEs, LEs, [LEs[-1]] * 120))

    # set life expectancies for years based on owner's current age
    currAge = iPropSpending['portfolioOwnerCurrentAge']
    LEs = LEs[currAge - 1:currAge - 1 + nyrs]

    # find spending proportions and ensure they are between 0 and 1 inclusive
    spendProps = 1.0 / LEs
    spendProps = np.maximum(spendProps, 0)
    spendProps = np.minimum(spendProps, 1)

    # if desired, show proportions spent
    if iPropSpending['showProportionsSpent'].lower() == 'y':
        fig2 = plt.figure()
        plt.rcParams.update({'font.size': 30})
        ss = client['figurePosition']
        fig2.set_size_inches(ss[2] / fig2.dpi, ss[3] / fig2.dpi)
        fig2.patch.set_facecolor('white')
        xs = np.arange(1, nyrs + 1)
        ys = spendProps
        plt.plot(xs, ys, '-*r', linewidth=2)
        plt.title('Proportions of Portfolio Spent', fontsize=40, color='b')
        plt.xlabel('Year', fontsize=30)
        plt.ylabel('Proportion of Portfolio Value Spent', fontsize=30)
        plt.grid()
        plt.show()

    # if desired, show Lockbox Equivalent Values
    if iPropSpending['showLockboxEquivalentValues'].lower() == 'y':
        # find lockbox equivalent values
        facs = 1 - spendProps
        facs = np.insert(facs, 0, 1)
        facs = facs[:-1]
        lbVals = np.cumprod(facs) * spendProps
        lbVals = lbVals * iPropSpending['investedAmount']
        fig3 = plt.figure()
        plt.rcParams.update({'font.size': 30})
        ss = client['figurePosition']
        fig3.set_size_inches(ss[2] / fig3.dpi, ss[3] / fig3.dpi)
        fig3.patch.set_facecolor('white')
        plt.bar(np.arange(len(lbVals)), lbVals, color='r', linewidth=2)
        plt.title('Lockbox Equivalent Initial Values', fontsize=40, color='b')
        plt.xlabel('Year', fontsize=30)
        plt.ylabel('Lockbox Equivalent Initial Value', fontsize=30)
        plt.grid()
        plt.show()

        # create blank screen
        figblank = plt.figure()
        figblank.set_size_inches(ss[2] / figblank.dpi, ss[3] / figblank.dpi)
        figblank.patch.set_facecolor('white')

    # create vector of initial portfolio values
    portvals = np.ones((nscen, 1)) * iPropSpending['investedAmount']

    # initialize incomes and fees matrices
    incsM = np.zeros((nscen, nyrs))
    feesM = np.zeros((nscen, nyrs))
    # compute incomes paid at the beginning of year 1
    incsM[:, 0] = portvals * spendProps[0]
    # compute portfolio values after income payments
    portvals = portvals - incsM[:, 0]

    # compute incomes and fees paid at beginning of each subsequent year
    for yr in range(1, nyrs):
        # compute portfolio values before deductions
        portvals = portvals * retsM[:, yr - 1]
        # compute and deduct fees paid at beginning of year
        feesV = (1 - rr) * portvals
        feesM[:, yr] = feesM[:, yr] + feesV
        portvals = portvals - feesV
        # compute incomes paid out at beginning of year in states 1, 2 or 3
        v = (client['pStatesM'][:, yr] > 0) & (client['pStatesM'][:, yr] < 4)
        incsM[:, yr] = v * (portvals * spendProps[yr])
        # pay entire value if state 4
        v = (client['pStatesM'][:, yr] == 4)
        incsM[:, yr] = incsM[:, yr] + v * portvals
        # deduct incomes paid from portfolio values
        portvals = portvals - incsM[:, yr]

    # add incomes and fees to client matrices
    client['incomesM'] = client['incomesM'] + incsM
    client['feesM'] = client['feesM'] + feesM

    return client

