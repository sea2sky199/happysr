import numpy as np

def iLBSplusDFA_process(client, iLBSplusDFA, market):

    # process lockbox spending plus deferred fixed annuity 
  
    # create deferred fixed annuity with cost equal to 50% of total 

    iFixedAnnuity = iFixedAnnuity_create()

    # set deferral period
    nLByrs = iLBSplusDFA['numberOfLockboxYears']
    iFixedAnnuity['guaranteedIncomes'] = np.zeros(nLByrs)

    # set relative incomes equal for personal states 1,2 and 3
    iFixedAnnuity['pStateIncomes'] = [0, 1, 1, 1, 0]

    # set incomes constant
    iFixedAnnuity['graduationRatio'] = 1.00

    # set type of income to real
    iFixedAnnuity['realOrNominal'] = 'r'

    # set ratio of value to initial cost
    iFixedAnnuity['valueOverCost'] = iLBSplusDFA['annuityValueOverCost']

    # cost
    iFixedAnnuity['cost'] = 0.50 * iLBSplusDFA['amountInvested']

    # create a temporary client with zero incomes
    clientTemp = client.copy()
    nscen, nyrs = clientTemp['incomesM'].shape
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))

    # process deferred fixed annuity with temporary client
    clientTemp = iFixedAnnuity_process(iFixedAnnuity, clientTemp, market)

    # find annuity real income per dollar invested
    annuityIncomePerDollar = np.max(clientTemp['incomesM']) / iFixedAnnuity['cost']

    # create lockbox spending with cost equal to 50% of total
    iLockboxSpending = iLockboxSpending_create()

    # set lockbox proportions for selected number of years
    props = iLBSplusDFA['lockboxProportions'][:, :nLByrs]
    iLockboxSpending['lockboxProportions'] = props

    # set initial investment
    iLockboxSpending['investedAmount'] = 0.50 * iLBSplusDFA['amountInvested']

    # bequest utility ratio
    iLockboxSpending['bequestUtilityRatio'] = iLBSplusDFA['bequestUtilityRatio']

    # show lockbox amounts (y or n)
    iLockboxSpending['showLockboxAmounts'] = 'n'

    # create a new temporary client with zero incomes
    clientTemp = client.copy()
    nscen, nyrs = clientTemp['incomesM'].shape
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))

    # process lockbox spending with temporary client
    clientTemp, iLockboxSpending = iLockboxSpending_process(iLockboxSpending, clientTemp, market)

    # find incomes in final year per dollar invested
    pstates = clientTemp['pStatesM'][:, nLByrs - 1]
    ii = np.where((pstates > 0) & (pstates < 4))
    incs = clientTemp['incomesM'][ii, nLByrs - 1]
    incs = np.sort(incs)[::-1]
    incsPerDollar = incs / iLockboxSpending['investedAmount']
    numIncsPerDollar = len(incsPerDollar)

    # find percentile of income in final year per dollar invested
    pctl = iLBSplusDFA['percentileOfLastLockboxYear']
    incNum = round(0.01 * pctl * numIncsPerDollar)
    if incNum < 1:
        incNum = 1
    if incNum > numIncsPerDollar:
        incNum = numIncsPerDollar
    LBIncomePerDollar = incsPerDollar[incNum - 1]

    # find amounts to invest in lockbox and deferred annuity
    r = annuityIncomePerDollar / (LBIncomePerDollar + annuityIncomePerDollar)
    LBInvestment = r * iLBSplusDFA['amountInvested']
    DFAInvestment = iLBSplusDFA['amountInvested'] - LBInvestment

    # create incomes from deferred fixed annuity
    clientTemp = client.copy()
    nscen, nyrs = clientTemp['incomesM'].shape
    iFixedAnnuity['cost'] = DFAInvestment
    clientTemp = iFixedAnnuity_process(iFixedAnnuity, clientTemp, market)
    DFAincsM = clientTemp['incomesM']
    feesM = clientTemp['feesM']

    # create incomes from lockbox spending
    clientTemp = client.copy()
    nscen, nyrs = clientTemp['incomesM'].shape
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))
    iLockboxSpending['investedAmount'] = LBInvestment
    clientTemp, iLockboxSpending = iLockboxSpending_process(iLockboxSpending, clientTemp, market)
    LBincsM = clientTemp['incomesM']

    # add amounts invested to iLBSplusDFA data structure
    iLBSplusDFA['DFAInvestment'] = DFAInvestment
    iLBSplusDFA['LBInvestment'] = LBInvestment
	
	# add incomes to client income matrix
    client['incomesM'] = client['incomesM'] + DFAincsM + LBincsM
    client['feesM'] = client['feesM'] + feesM

    return client, iLBSplusDFA

