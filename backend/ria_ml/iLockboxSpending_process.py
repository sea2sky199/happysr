import numpy as np
import matplotlib.pyplot as plt

def iLockboxSpending_process(iLockboxSpending, client, market):
    nscen, nyrs = client['pStatesM'].shape

    props = np.array(iLockboxSpending['lockboxProportions'], dtype=float)
    nlbyears = props.shape[1]
    if nlbyears < nyrs:
        props = np.hstack([props, np.zeros((2, nyrs - nlbyears))])
    if props.shape[1] > nyrs:
        props = props[:, :nyrs]

    surv1 = np.cumprod(1 - client['mortP1'])
    surv2 = np.cumprod(1 - client['mortP2'])
    survboth = surv1 * surv2
    surv1only = surv1 * (1 - surv2)
    surv2only = surv2 * (1 - surv1)
    survanyone = survboth + surv1only + surv2only

    ranyoneV = np.exp(np.log(survanyone) / market['b'])
    rmaxV = np.ones(nyrs)
    bur = iLockboxSpending['bequestUtilityRatio']
    ratioV = bur * rmaxV + (1 - bur) * ranyoneV
    oldsum = np.sum(props[1, :])
    newmktprops = ratioV * props[1, :]
    newsum = np.sum(newmktprops)
    if newsum > 0:
        newmktprops = (newmktprops / newsum) * oldsum
    newprops = np.vstack([props[0, :], newmktprops])
    iLockboxSpending['adjustedLockboxProportions'] = newprops

    LBVals = (newprops / np.sum(newprops)) * iLockboxSpending['investedAmount']

    if iLockboxSpending['showLockboxAmounts'].lower() == 'y':
        plt.figure()
        x = np.arange(1, LBVals.shape[1] + 1)
        plt.bar(x, LBVals[0, :], label='TIPS')
        plt.bar(x, LBVals[1, :], bottom=LBVals[0, :], label='Market')
        plt.grid(True)
        plt.xlabel('Lockbox Maturity Year')
        plt.ylabel('Amount Invested at Inception')
        plt.legend(['TIPS', 'Market'])
        plt.title('Lockbox Amounts at Inception', color='b')
        plt.show()

    incsM = np.zeros((nscen, nyrs))
    for yr in range(nyrs):
        ii = np.where((client['pStatesM'][:, yr] > 0) & (client['pStatesM'][:, yr] < 4))[0]
        incsM[ii, yr] = (LBVals[0, yr] * market['cumRfsM'][ii, yr] +
                         LBVals[1, yr] * market['cumRmsM'][ii, yr])
        ii = np.where(client['pStatesM'][:, yr] == 4)[0]
        m = np.sum(LBVals[:, yr:], axis=1)
        incsM[ii, yr] = (m[0] * market['cumRfsM'][ii, yr] +
                         m[1] * market['cumRmsM'][ii, yr])

    client['incomesM'] = client['incomesM'] + incsM
    return client, iLockboxSpending
