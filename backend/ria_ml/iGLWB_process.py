import numpy as np

def iGLWB_process(client, market, iGLWB):
    initialValue = iGLWB['initialValue']
    expPropTWB = iGLWB['expenseRatioOfTWB']
    expPropFund = iGLWB['expenseRatioOfFund']

    minAge = min(client['p1Age'], client['p2Age'])
    if iGLWB['singleOrJoint'].lower() == 'j':
        tbl = iGLWB['jointLifeWithdrawalRates']
    else:
        tbl = iGLWB['singleLifeWithdrawalRates']
    rows = (minAge >= tbl[:, 0]) & (minAge <= tbl[:, 1])
    withdrawPropTWB = np.sum(rows * tbl[:, 2])

    nrmsM = market['rmsM'] * market['csM']
    nscen, nyrs = client['incomesM'].shape

    portvalV = initialValue * np.ones(nscen)
    twbV = portvalV.copy()

    incsM = np.zeros((nscen, nyrs))
    feesFundM = np.zeros((nscen, nyrs))
    feesRiderM = np.zeros((nscen, nyrs))

    incsM[:, 0] = withdrawPropTWB * twbV
    portvalV -= incsM[:, 0]

    for yr in range(1, nyrs):
        ii = np.where((client['pStatesM'][:, yr] > 0) & (client['pStatesM'][:, yr] < 4))[0]
        if len(ii) > 0:
            portvalV[ii] *= nrmsM[ii, yr - 1]
            feesFundM[ii, yr] = expPropFund * portvalV[ii]
            portvalV[ii] -= feesFundM[ii, yr]
            incsM[ii, yr] = withdrawPropTWB * twbV[ii]
            portvalV[ii] -= incsM[ii, yr]
            feesRiderM[ii, yr] = expPropTWB * twbV[ii]
            portvalV[ii] -= feesRiderM[ii, yr]
            negvalV = np.minimum(portvalV[ii], 0)
            feesRiderM[ii, yr] += negvalV
            portvalV[ii] -= negvalV
            twbV[ii] = np.maximum(portvalV[ii], twbV[ii])

        ii = np.where(client['pStatesM'][:, yr] == 4)[0]
        if len(ii) > 0:
            portvalV[ii] *= nrmsM[ii, yr - 1]
            feesFundM[ii, yr] = expPropFund * portvalV[ii]
            portvalV[ii] -= feesFundM[ii, yr]
            incsM[ii, yr] = portvalV[ii]
            portvalV[ii] -= incsM[ii, yr]

    rincsM = incsM / market['cumCsM']
    rfeesRiderM = feesRiderM / market['cumCsM']
    rfeesFundM = feesFundM / market['cumCsM']

    client['incomesM'] = client['incomesM'] + rincsM
    client['feesM'] = client['feesM'] + rfeesRiderM + rfeesFundM

    if iGLWB['saveFeeMatrices'].lower() == 'y':
        iGLWB['feesRiderM'] = rfeesRiderM
        iGLWB['feesFundM'] = rfeesFundM

    return client, iGLWB
