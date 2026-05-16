import numpy as np
import matplotlib.pyplot as plt

def iLockboxSpending_process(iLockboxSpending, client, market):

    # creates LB spending income matrix and fees matrix
    # then adds values to client incomes matrix and fees matrices
  
    # the lockbox proportions matrix can be computed by AMDnLockboxes_process
    # or in some other manner. The first row is TIPS, the second is Market
    #  proportions, and there is a column for each year in the client matrix

    # get number of scenarios and years
    nscen, nyrs = client['pStatesM'].shape

    # fill lockbox proportions with zeros if needed
    props = iLockboxSpending['lockboxProportions']
    nlbyears = props.shape[1]
    props = np.hstack([props[:, :nlbyears], np.zeros((2, nyrs - nlbyears))])
    if props.shape[1] > nyrs:
        props = props[:, :nyrs]

    # compute survival rates
    surv1 = np.cumprod(1 - client['mortP1'])
    surv2 = np.cumprod(1 - client['mortP2'])
    survboth = surv1 * surv2
    surv1only = surv1 * (1 - surv2)
    surv2only = surv2 * (1 - surv1)
    survanyone = survboth + surv1only + surv2only

    # adjust proportions to take bequest utility ratio into account
    # adjust market lockbox values
    ranyoneV = np.exp(np.log(survanyone) / market['b'])
    rmaxV = np.ones(nyrs)
    bur = iLockboxSpending['bequestUtilityRatio']
    ratioV = bur * rmaxV + (1 - bur) * ranyoneV
    # change market proportions to keep total the same
    oldsum = np.sum(props[1, :])
    newmktprops = ratioV * props[1, :]
    newsum = np.sum(newmktprops)
    newmktprops = (newmktprops / newsum) * oldsum
    newprops = np.vstack([props[0, :], newmktprops])
    # save new proportions
    iLockboxSpending['adjustedLockboxProportions'] = newprops

    # compute lockbox dollar values
    LBVals = (newprops / np.sum(newprops)) * iLockboxSpending['investedAmount']

    # plot lockbox amounts if requested
    if iLockboxSpending['showLockboxAmounts'].lower() == 'y':
        xs = LBVals
        nyrs = xs.shape[1]
        fig, ax = plt.subplots()
        x = np.arange(1, nyrs + 1)
        ax.bar(x, xs.T, stacked=True)
        ax.grid(True)
        ax.set_fontsize(30)
        ss = client['figurePosition']
        fig.set_size_inches(ss[2] / 100, ss[3] / 100)
        fig.patch.set_facecolor('white')
        ax.set_xlabel('Lockbox Maturity Year', fontsize=30)
        ax.set_ylabel('Amount Invested at Inception', fontsize=30)
        ax.legend(['TIPS', 'Market'])
        ax.set_xlim([0, nyrs + 1])
        ax.set_ylim([0, np.max(np.sum(xs, axis=0))])
        ax.set_title('Lockbox Amounts at Inception', fontsize=40, color='b')
        plt.show()

    # create incomes
    incsM = np.zeros((nscen, nyrs))
    for yr in range(nyrs):
        # scenarios with anyone alive
        ii = np.where((client['pStatesM'][:, yr] > 0) & (client['pStatesM'][:, yr] < 4))[0]
        # add cumulative value of tips
        incsM[ii, yr] = LBVals[0, yr] * market['cumRfsM'][ii, yr]
        # add cumulative value of market
        incsM[ii, yr] += LBVals[1, yr] * market['cumRmsM'][ii, yr]
        # scenarios with estate
        ii = np.where(client['pStatesM'][:, yr] == 4)[0]
        # values of current and remaining lockboxes
        m = np.sum(LBVals[:, yr:], axis=1)
        # add cumulative values of tips
        incsM[ii, yr] = m[0] * market['cumRfsM'][ii, yr]
        # add cumulative value of market
        incsM[ii, yr] += m[1] * market['cumRmsM'][ii, yr]

    # add incomes to client incomes matrix
    client['incomesM'] += incsM

    return client, iLockboxSpending