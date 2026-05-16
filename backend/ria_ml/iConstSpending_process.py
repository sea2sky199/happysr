import numpy as np
import matplotlib.pyplot as plt

def iConstSpending_process(iConstSpending, client, market):
    nscen, nyrs = market['rmsM'].shape
    path = np.array(iConstSpending['glidePath'])

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
    pathxs = np.array(pathxs)
    pathys = np.array(pathys)

    if iConstSpending['showGlidePath'].lower() == 'y':
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

    rr = iConstSpending['retentionRatio']
    portvals = np.ones(nscen) * iConstSpending['investedAmount']

    desiredSpendingM = np.zeros((nscen, nyrs))
    prop = iConstSpending['initialProportionSpent']
    amt = prop * iConstSpending['investedAmount']
    gradRatio = iConstSpending['graduationRatio']
    factors = gradRatio**np.arange(nyrs)
    maxSpendingM = np.outer(np.ones(nscen), amt * factors)

    props = np.array(iConstSpending['pStateRelativeIncomes'], dtype=float)
    props = props / np.max(props)
    props = np.maximum(props, 0)
    for ps in range(1, 4):
        s = maxSpendingM * props[ps - 1]
        m = (client['pStatesM'] == ps) * s
        desiredSpendingM += m

    incsM = np.zeros((nscen, nyrs))
    feesM = np.zeros((nscen, nyrs))

    incsM[:, 0] = np.minimum(desiredSpendingM[:, 0], portvals)
    portvals -= incsM[:, 0]

    for yr in range(1, nyrs):
        portvals = portvals * retsM[:, yr - 1]
        feesV = (1 - rr) * portvals
        feesM[:, yr] = feesV
        portvals -= feesV
        v = (client['pStatesM'][:, yr] > 0) & (client['pStatesM'][:, yr] < 4)
        incsM[:, yr] = v * np.minimum(desiredSpendingM[:, yr], portvals)
        v = (client['pStatesM'][:, yr] == 4)
        incsM[:, yr] += v * portvals
        portvals -= incsM[:, yr]

    client['incomesM'] = client['incomesM'] + incsM
    client['feesM'] = client['feesM'] + feesM
    return client
