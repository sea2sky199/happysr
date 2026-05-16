import numpy as np
from iLockboxSpending_create import iLockboxSpending_create
from iLockboxSpending_process import iLockboxSpending_process
from iFAPlockbox_create import iFAPlockbox_create
from iFAPlockbox_process import iFAPlockbox_process

def iLBSplusFAP_process(client, iLBSplusFAP, market):
    nscen, nyrs = client['incomesM'].shape

    iLockboxSpending = iLockboxSpending_create()
    iLockboxSpending['lockboxProportions'] = np.array(iLBSplusFAP['lockboxProportions'])
    lastSpendingYr = iLBSplusFAP['annuitizationYear'] - 1
    iLockboxSpending['lockboxProportions'] = iLockboxSpending['lockboxProportions'][:, :lastSpendingYr]
    iLockboxSpending['bequestUtilityRatio'] = iLBSplusFAP['bequestUtilityRatio']
    iLockboxSpending['showLockboxAmounts'] = 'n'
    iLockboxSpending['investedAmount'] = 0.50 * iLBSplusFAP['amountInvested']

    clientTemp = {k: (v.copy() if isinstance(v, np.ndarray) else v)
                  for k, v in client.items()}
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))
    clientTemp, _ = iLockboxSpending_process(iLockboxSpending, clientTemp, market)

    ps = clientTemp['pStatesM'][:, lastSpendingYr - 1]
    ii = np.where((ps > 0) & (ps < 4))[0]
    incs = clientTemp['incomesM'][ii, lastSpendingYr - 1]
    sortincs = np.sort(incs)[::-1]
    matchPctl = np.clip(iLBSplusFAP['incomePercentileToMatch'] / 100, 0, 1)
    n = int(round(matchPctl * len(sortincs)))
    n = max(1, min(n, len(sortincs)))
    pctlIncSpending = sortincs[n - 1]

    iFAPlockbox = iFAPlockbox_create()
    iFAPlockbox['yearOfAnnuityPurchase'] = iLBSplusFAP['annuitizationYear']
    iFAPlockbox['proportionInTIPS'] = iLBSplusFAP['FAPlockboxProportionInTIPS']
    iFAPlockbox['investedAmount'] = 0.50 * iLBSplusFAP['amountInvested']
    iFAPlockbox['annuityValueOverCost'] = iLBSplusFAP['annuityValueOverCost']

    clientTemp = {k: (v.copy() if isinstance(v, np.ndarray) else v)
                  for k, v in client.items()}
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))
    clientTemp = iFAPlockbox_process(clientTemp, iFAPlockbox, market)

    ps2 = clientTemp['pStatesM'][:, lastSpendingYr]
    ii2 = np.where((ps2 > 0) & (ps2 < 4))[0]
    incs2 = clientTemp['incomesM'][ii2, lastSpendingYr]
    sortincs2 = np.sort(incs2)[::-1]
    n2 = int(round(matchPctl * len(sortincs2)))
    n2 = max(1, min(n2, len(sortincs2)))
    pctlIncAnnuity = sortincs2[n2 - 1]

    incomePerDollarSpending = pctlIncSpending / iLockboxSpending['investedAmount']
    incomePerDollarAnnuity = pctlIncAnnuity / iFAPlockbox['investedAmount']
    total = incomePerDollarSpending + incomePerDollarAnnuity
    propSpending = incomePerDollarAnnuity / total
    propAnnuity = incomePerDollarSpending / total
    totAmountInvested = iLockboxSpending['investedAmount'] + iFAPlockbox['investedAmount']

    iLockboxSpending['investedAmount'] = propSpending * totAmountInvested
    iFAPlockbox['investedAmount'] = propAnnuity * totAmountInvested
    iLBSplusFAP['spendingAmountInvested'] = iLockboxSpending['investedAmount']
    iLBSplusFAP['FAPAmountInvested'] = iFAPlockbox['investedAmount']

    clientTemp = {k: (v.copy() if isinstance(v, np.ndarray) else v)
                  for k, v in client.items()}
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))
    clientTemp, iLockboxSpending = iLockboxSpending_process(iLockboxSpending, clientTemp, market)
    clientTemp = iFAPlockbox_process(clientTemp, iFAPlockbox, market)

    client['incomesM'] = client['incomesM'] + clientTemp['incomesM']
    client['feesM'] = client['feesM'] + clientTemp['feesM']
    return client, iLBSplusFAP
