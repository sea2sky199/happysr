import numpy as np

def iLBSplusFAP_process(client, iLBSplusFAP, market):
    # Create a temporary client
    clientTemp = client.copy()

    # Process lockbox spending with 0.5 of the total amount invested
    iLockboxSpending = iLockboxSpending_create()

    # Set lockbox proportions
    iLockboxSpending.lockboxProportions = iLBSplusFAP.lockboxProportions

    # Use lockbox spending up to and including the year before annuity purchase
    lastSpendingYr = iLBSplusFAP.annuitizationYear - 1
    iLockboxSpending.lockboxProportions = iLockboxSpending.lockboxProportions[:, :lastSpendingYr]

    # Set bequest utility ratio
    iLockboxSpending.bequestUtilityRatio = iLBSplusFAP.bequestUtilityRatio

    # Do not show lockbox proportions
    iLockboxSpending.showLockboxAmounts = 'n'

    # Amount invested for lockbox spending
    iLockboxSpending.investedAmount = 0.50 * iLBSplusFAP.amountInvested

    # Process lockbox spending
    clientTemp = client.copy()
    nscen, nyrs = client.incomesM.shape
    clientTemp.incomesM = np.zeros((nscen, nyrs))
    clientTemp = iLockboxSpending_process(iLockboxSpending, clientTemp, market)

    # Find percentile income in last lockbox spending year for matching states
    ps = clientTemp.pStatesM[:, lastSpendingYr]
    ii = np.where((ps > 0) & (ps < 4))[0]
    incs = clientTemp.incomesM[ii, lastSpendingYr]
    sortincs = np.sort(incs)[::-1]
    matchPctl = iLBSplusFAP.incomePercentileToMatch / 100
    matchPctl = max(0, min(1, matchPctl))
    n = round(matchPctl * len(sortincs))
    n = max(1, min(n, len(sortincs)))
    pctlIncSpending = sortincs[n - 1]

    # Create lockbox for future annuity purchase
    iFAPlockbox = iFAPlockbox_create()

    # Set year annuity is to be purchased
    iFAPlockbox.yearOfAnnuityPurchase = iLBSplusFAP.annuitizationYear

    # Set initial proportion in TIPS in the FAPlockbox
    propTIPS = iLBSplusFAP.FAPlockboxProportionInTIPS
    iFAPlockbox.proportionInTIPS = propTIPS

    # Set initial amount ($) in the lockbox
    iFAPlockbox.investedAmount = 0.50 * iLBSplusFAP.amountInvested

    # Process FAP lockbox with temporary client
    clientTemp = client.copy()
    nscen, nyrs = client.incomesM.shape
    clientTemp.incomesM = np.zeros((nscen, nyrs))
    clientTemp = iFAPlockbox_process(clientTemp, iFAPlockbox, market)

    # Find percentile amount spent in first annuity year matching states
    ps = clientTemp.pStatesM[:, lastSpendingYr + 1]
    incs = clientTemp.incomesM[ii, lastSpendingYr + 1]
    sortincs = np.sort(incs)[::-1]
    n = round(matchPctl * len(sortincs))
    n = max(1, min(n, len(sortincs)))
    pctlIncAnnuity = sortincs[n - 1]

    # Compute revised amounts to be invested
    # Find incomes per dollar
    incomePerDollarSpending = pctlIncSpending / iLockboxSpending.investedAmount
    incomePerDollarAnnuity = pctlIncAnnuity / iFAPlockbox.investedAmount

    # Find proportions of total investment
    total_income_per_dollar = incomePerDollarSpending + incomePerDollarAnnuity
    propSpending = incomePerDollarAnnuity / total_income_per_dollar
    propAnnuity = incomePerDollarSpending / total_income_per_dollar

    # Find total amount invested
    totAmountInvested = iLockboxSpending.investedAmount + iFAPlockbox.investedAmount

    # Put amounts to be invested in data structures
    iLockboxSpending.investedAmount = propSpending * totAmountInvested
    iFAPlockbox.investedAmount = propAnnuity * totAmountInvested

    # Add to iLBSplusFAP data structure
    iLBSplusFAP.spendingAmountInvested = iLockboxSpending.investedAmount
    iLBSplusFAP.FAPAmountInvested = iFAPlockbox.investedAmount

    # Create incomes from lockbox spending
    clientTemp = client.copy()
    nscen, nyrs = clientTemp.incomesM.shape
    clientTemp.incomesM = np.zeros((nscen, nyrs))
	
    clientTemp, iLockboxSpending = iLockboxSpending_process(iLockboxSpending, clientTemp, market)

    # add incomes and fees from FAP
    clientTemp = iFAPlockbox_process(clientTemp, iFAPlockbox, market)

    # add incomes to client income matrix
    client['incomesM'] += clientTemp['incomesM']
    # add fees to client fee matrix
    client['feesM'] += clientTemp['feesM']

    return client, iLBSplusFAP