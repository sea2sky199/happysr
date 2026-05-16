import numpy as np
from iFixedAnnuity_create import iFixedAnnuity_create
from iFixedAnnuity_process import iFixedAnnuity_process
from iLockboxSpending_create import iLockboxSpending_create
from iLockboxSpending_process import iLockboxSpending_process

def iLBSplusDFA_process(client, iLBSplusDFA, market):
    iFixedAnnuity = iFixedAnnuity_create()
    nLByrs = iLBSplusDFA['numberOfLockboxYears']
    iFixedAnnuity['guaranteedIncomes'] = np.zeros(nLByrs)
    iFixedAnnuity['pStateIncomes'] = [0, 1, 1, 1, 0]
    iFixedAnnuity['graduationRatio'] = 1.00
    iFixedAnnuity['realOrNominal'] = 'r'
    iFixedAnnuity['valueOverCost'] = iLBSplusDFA['annuityValueOverCost']
    iFixedAnnuity['cost'] = 0.50 * iLBSplusDFA['amountInvested']

    clientTemp = {k: (v.copy() if isinstance(v, np.ndarray) else v)
                  for k, v in client.items()}
    nscen, nyrs = clientTemp['incomesM'].shape
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))
    clientTemp = iFixedAnnuity_process(iFixedAnnuity, clientTemp, market)
    annuityIncomePerDollar = np.max(clientTemp['incomesM']) / iFixedAnnuity['cost']

    iLockboxSpending = iLockboxSpending_create()
    props = np.array(iLBSplusDFA['lockboxProportions'])[:, :nLByrs]
    iLockboxSpending['lockboxProportions'] = props
    iLockboxSpending['investedAmount'] = 0.50 * iLBSplusDFA['amountInvested']
    iLockboxSpending['bequestUtilityRatio'] = iLBSplusDFA['bequestUtilityRatio']
    iLockboxSpending['showLockboxAmounts'] = 'n'

    clientTemp = {k: (v.copy() if isinstance(v, np.ndarray) else v)
                  for k, v in client.items()}
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))
    clientTemp, iLockboxSpending = iLockboxSpending_process(iLockboxSpending, clientTemp, market)

    pstates = clientTemp['pStatesM'][:, nLByrs - 1]
    ii = np.where((pstates > 0) & (pstates < 4))[0]
    incs = clientTemp['incomesM'][ii, nLByrs - 1]
    incs = np.sort(incs)[::-1]
    incsPerDollar = incs / iLockboxSpending['investedAmount']
    numIncsPerDollar = len(incsPerDollar)

    pctl = iLBSplusDFA['percentileOfLastLockboxYear']
    incNum = int(round(0.01 * pctl * numIncsPerDollar))
    incNum = max(1, min(incNum, numIncsPerDollar))
    LBIncomePerDollar = incsPerDollar[incNum - 1]

    r = annuityIncomePerDollar / (LBIncomePerDollar + annuityIncomePerDollar)
    LBInvestment = r * iLBSplusDFA['amountInvested']
    DFAInvestment = iLBSplusDFA['amountInvested'] - LBInvestment

    clientTemp = {k: (v.copy() if isinstance(v, np.ndarray) else v)
                  for k, v in client.items()}
    iFixedAnnuity['cost'] = DFAInvestment
    clientTemp = iFixedAnnuity_process(iFixedAnnuity, clientTemp, market)
    DFAincsM = clientTemp['incomesM'].copy()
    feesM = clientTemp['feesM'].copy()

    clientTemp = {k: (v.copy() if isinstance(v, np.ndarray) else v)
                  for k, v in client.items()}
    clientTemp['incomesM'] = np.zeros((nscen, nyrs))
    iLockboxSpending['investedAmount'] = LBInvestment
    clientTemp, iLockboxSpending = iLockboxSpending_process(iLockboxSpending, clientTemp, market)
    LBincsM = clientTemp['incomesM'].copy()

    iLBSplusDFA['DFAInvestment'] = DFAInvestment
    iLBSplusDFA['LBInvestment'] = LBInvestment

    client['incomesM'] = client['incomesM'] + DFAincsM + LBincsM
    client['feesM'] = client['feesM'] + feesM
    return client, iLBSplusDFA
