import numpy as np

def iGLWB_process(client, market, iGLWB):
    # set parameters
    initialValue = iGLWB['initialValue']
    expPropTWB = iGLWB['expenseRatioOfTWB']
    expPropFund = iGLWB['expenseRatioOfFund']

    # find proportion of TWB to withdraw
    minAge = min(client['p1Age'], client['p2Age'])
    if iGLWB['singleOrJoint'].lower() == 'j':
        tbl = iGLWB['jointLifeWithdrawalRates']
    else:
        tbl = iGLWB['singleLifeWithdrawalRates']

    rows = (tbl[:, 0] <= minAge) & (minAge <= tbl[:, 1])
    withdrawPropTWB = np.sum(rows * tbl[:, 2])

    # create matrix of nominal market returns
    nrmsM = market['rmsM'] * market['csM']

    # get matrix dimensions
    nscen, nyrs = client['incomesM'].shape

    # set initial portfolio value vector
    portvalV = initialValue * np.ones((nscen, 1))
    # set vector of total withdrawal bases
    twbV = portvalV.copy()

    # create nominal incomes and nominal fees matrices
    incsM = np.zeros((nscen, nyrs))
    feesFundM = np.zeros((nscen, nyrs))
    feesRiderM = np.zeros((nscen, nyrs))

    # set initial year payouts
    incsM[:, 0] = withdrawPropTWB * twbV[:, 0]
    # adjust portfolio values
    portvalV = portvalV - incsM[:, 0].reshape(-1, 1)
    # set initial year fees to zero
    feesFundM[:, 0] = np.zeros((nscen, 1))
    feesRiderM[:, 0] = np.zeros((nscen, 1))

    # do remaining years
    for yr in range(1, nyrs):
        # find scenarios in which one or two are alive
        ii = np.where((client['pStatesM'][:, yr] > 0) & (client['pStatesM'][:, yr] < 4))[0]
        if len(ii) > 0:
            # increment nominal values of portfolio
            portvalV[ii] = portvalV[ii] * nrmsM[ii, yr - 1]
            # compute fees for fund and subtract from portfolio value
            feesFundM[ii, yr] = expPropFund * portvalV[ii]
            portvalV[ii] = portvalV[ii] - feesFundM[ii, yr]
            # compute guaranteed withdrawals and add to incomes
            incsM[ii, yr] = withdrawPropTWB * twbV[ii]
            # subtract withdrawals from portfolio values
            portvalV[ii] = portvalV[ii] - incsM[ii, yr]
            # compute rider fees
            feesRiderM[ii, yr] = expPropTWB * twbV[ii]
            # subtract rider fees from portfolio values
            portvalV[ii] = portvalV[ii] - feesRiderM[ii, yr]
            # for negative portfolio values, adjust rider fees
            negvalV = np.zeros((nscen, 1))
            negvalV[ii] = np.minimum(portvalV[ii], 0)
            feesRiderM[ii, yr] = feesRiderM[ii, yr] + negvalV[ii]
            portvalV[ii] = portvalV[ii] - negvalV[ii]
            # set TWB values to max of portfolio values and prior TWB
            twbV[ii] = np.maximum(portvalV[ii], twbV[ii])

        # scenarios in which estate is paid
        ii = np.where(client['pStatesM'][:, yr] == 4)[0]
        if len(ii) > 0:
            # increment nominal values of portfolio
            portvalV[ii] = portvalV[ii] * nrmsM[ii, yr - 1]
            # compute fees for fund and subtract from portfolio value
            feesFundM[ii, yr] = expPropFund * portvalV[ii]
            portvalV[ii] = portvalV[ii] - feesFundM[ii, yr]
            # pay remaining portfolio value to estate
            incsM[ii, yr] = portvalV[ii]
            portvalV[ii] = portvalV[ii] - incsM[ii, yr]

    # convert nominal incomes matrix to real
    rincsM = incsM / market['cumCsM']
    # convert nominal fees matrices to real fees
    rfeesRiderM = feesRiderM / market['cumCsM']
    rfeesFundM = feesFundM / market['cumCsM']
    # add results to client income and fee matrices
    client['incomesM'] = client['incomesM'] + rincsM
    client['feesM'] = client['feesM'] + rfeesRiderM + rfeesFundM

    return client, iGLWB

