import numpy as np
import matplotlib.pyplot as plt

def iPropSpending_process(iPropSpending, client, market):
    nscen, nyrs = market['rmsM'].shape
    path = np.array(iPropSpending['glidePath'])

    ys = path[0, :]
    xs = path[1, :]
    xs = np.maximum(xs, 1)
    ys = np.minimum(ys, 1)
    ys = np.maximum(ys, 0)
    order = np.argsort(xs)
    xs = xs[order]
    ys = ys[order]
    if xs[0] > 1:
        xs = np.concatenate([[1], xs])
        ys = np.concatenate([[ys[0]], ys])
    if xs[-1] < nyrs:
        xs = np.concatenate([xs, [nyrs]])
        ys = np.concatenate([ys, [ys[-1]]])

    pathxs = []
    pathys = []
    for i in range(len(xs) - 1):
        xlft, xrt = xs[i], xs[i + 1]
        ylft, yrt = ys[i], ys[i + 1]
        pathxs.append(xlft)
        pathys.append(ylft)
        if xlft != xrt:
            slope = (yrt - ylft) / (xrt - xlft)
            for x in range(int(xlft) + 1, int(xrt)):
                pathxs.append(x)
                pathys.append(ylft + slope * (x - xlft))
    pathxs.append(xs[-1])
    pathys.append(ys[-1])
    pathys = np.array(pathys)

    if iPropSpending['showGlidePath'].lower() == 'y':
        plt.figure()
        plt.xlabel('Year')
        plt.ylabel('Proportion in Market Portfolio')
        plt.plot(path[1, :], path[0, :], '*b', linewidth=4)
        plt.plot(xs, ys, '-r', linewidth=2)
        plt.legend(['Input', 'All'])
        plt.axis([0, nyrs + 1, 0, 1])
        plt.title('Glide Path: Market Proportions by Year', color='b')
        plt.grid(True)
        plt.show()

    retsM = np.zeros((nscen, nyrs))
    for yr in range(nyrs - 1):
        rets = pathys[yr] * market['rmsM'][:, yr]
        rets = rets + (1 - pathys[yr]) * market['rfsM'][:, yr]
        retsM[:, yr] = rets

    rr = iPropSpending['retentionRatio']

    if iPropSpending['useRMDlifeExpectancies'].lower() == 'y':
        LEs = np.array([27.4, 26.5, 25.6, 24.7, 23.8, 22.9, 22.0, 21.2, 20.3, 19.5,
                        18.7, 17.9, 17.1, 16.3, 15.5, 14.8, 14.1, 13.4, 12.7, 12.0,
                        11.4, 10.8, 10.2,  9.6,  9.1,  8.6,  8.1,  7.6,  7.1,  6.7,
                         6.3,  5.9,  5.5,  5.2,  4.9,  4.5,  4.2,  3.9,  3.7,  3.4,
                         3.1,  2.9,  2.6,  2.4,  2.1,  1.9])
        firstLEAge = 70
    else:
        LEs = np.array(iPropSpending['nonRMDlifeExpectancies'])
        firstLEAge = iPropSpending['nonRMDfirstLEAge']

    firstLE = LEs[0]
    initLEs = firstLE + np.arange(firstLEAge - 1, 0, -1)
    LEs = np.concatenate([initLEs, LEs])
    LEs = np.concatenate([LEs, LEs[-1] * np.ones(120)])
    currAge = iPropSpending['portfolioOwnerCurrentAge']
    LEs = LEs[currAge - 1:]
    LEs = LEs[:nyrs]

    spendProps = 1.0 / LEs
    spendProps = np.maximum(spendProps, 0)
    spendProps = np.minimum(spendProps, 1)

    if iPropSpending['showProportionsSpent'].lower() == 'y':
        plt.figure()
        plt.plot(np.arange(1, nyrs + 1), spendProps, '-*r', linewidth=2)
        plt.title('Proportions of Portfolio Spent', color='b')
        plt.xlabel('Year')
        plt.ylabel('Proportion of Portfolio Value Spent')
        plt.grid(True)
        plt.show()

    portvals = np.ones(nscen) * iPropSpending['investedAmount']
    incsM = np.zeros((nscen, nyrs))
    feesM = np.zeros((nscen, nyrs))

    incsM[:, 0] = portvals * spendProps[0]
    portvals -= incsM[:, 0]

    for yr in range(1, nyrs):
        portvals = portvals * retsM[:, yr - 1]
        feesV = (1 - rr) * portvals
        feesM[:, yr] += feesV
        portvals -= feesV
        v = (client['pStatesM'][:, yr] > 0) & (client['pStatesM'][:, yr] < 4)
        incsM[:, yr] = v * (portvals * spendProps[yr])
        v = (client['pStatesM'][:, yr] == 4)
        incsM[:, yr] += v * portvals
        portvals -= incsM[:, yr]

    client['incomesM'] = client['incomesM'] + incsM
    client['feesM'] = client['feesM'] + feesM
    return client
