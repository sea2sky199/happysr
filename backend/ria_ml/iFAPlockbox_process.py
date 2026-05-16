import numpy as np

def iFAPlockbox_process(client, iFAPlockbox, market):
    FAPyear = iFAPlockbox['yearOfAnnuityPurchase']
    mortP1 = client['mortP1'][FAPyear:]
    mortP2 = client['mortP2'][FAPyear:]

    probP1Alive = np.cumprod(1 - mortP1)
    probP2Alive = np.cumprod(1 - mortP2)
    probBothDead = (1 - probP1Alive) * (1 - probP2Alive)
    probPayment1 = np.concatenate([[1], probP1Alive])
    probPayment2 = np.concatenate([[1], probP2Alive])
    probPayment3 = np.concatenate([[1], 1 - probBothDead])

    n = len(probPayment1)
    dfs = market['rf']**np.arange(n)
    pvs = 1.0 / dfs
    valuePerDollar1 = np.sum(probPayment1 * pvs)
    valuePerDollar2 = np.sum(probPayment2 * pvs)
    valuePerDollar3 = np.sum(probPayment3 * pvs)

    valOverCost = iFAPlockbox['annuityValueOverCost']
    costPerDollar1 = valuePerDollar1 / valOverCost
    costPerDollar2 = valuePerDollar2 / valOverCost
    costPerDollar3 = valuePerDollar3 / valOverCost

    tipsProp = iFAPlockbox['proportionInTIPS']
    tipsProp = np.clip(tipsProp, 0, 1)
    tipsAmt = tipsProp * iFAPlockbox['investedAmount']
    mktAmt = iFAPlockbox['investedAmount'] - tipsAmt
    mktVals = mktAmt * market['cumRmsM'][:, FAPyear - 1]
    tipsVals = tipsAmt * market['cumRfsM'][:, FAPyear - 1]
    totVals = mktVals + tipsVals

    nscen, nyrs = client['incomesM'].shape
    annPayments = np.zeros(nscen)
    feesV = np.zeros(nscen)

    ii = np.where(client['pStatesM'][:, FAPyear - 1] == 1)[0]
    annPayments[ii] = totVals[ii] / costPerDollar1
    feesV[ii] = (1 - valOverCost) * totVals[ii]
    ii = np.where(client['pStatesM'][:, FAPyear - 1] == 2)[0]
    annPayments[ii] = totVals[ii] / costPerDollar2
    feesV[ii] = (1 - valOverCost) * totVals[ii]
    ii = np.where(client['pStatesM'][:, FAPyear - 1] == 3)[0]
    annPayments[ii] = totVals[ii] / costPerDollar3
    feesV[ii] = (1 - valOverCost) * totVals[ii]

    incsM = np.zeros((nscen, nyrs))
    incsM[:, FAPyear - 1] = annPayments
    for yr in range(FAPyear, nyrs):
        ps = client['pStatesM'][:, yr]
        v = (ps > 0) & (ps < 4)
        incsM[:, yr] = v * annPayments

    feesM = np.zeros((nscen, nyrs))
    feesM[:, FAPyear - 1] = feesV

    marketValsM = mktAmt * market['cumRmsM']
    tipsValsM = tipsAmt * market['cumRfsM']
    totValsM = marketValsM + tipsValsM
    totValsM[:, FAPyear:] = 0
    estatePaidM = (client['pStatesM'] == 4)
    amtsPdM = totValsM * estatePaidM

    client['incomesM'] = client['incomesM'] + incsM + amtsPdM
    client['feesM'] = client['feesM'] + feesM
    return client
