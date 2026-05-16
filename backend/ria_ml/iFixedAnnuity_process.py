import numpy as np

def iFixedAnnuity_process(iFixedAnnuity, client, market):
    nscen, nyrs = client['pStatesM'].shape

    psIncomesM = []
    guarIncomes_base = np.array(iFixedAnnuity['guaranteedIncomes'])
    nGuar = len(guarIncomes_base)
    nAnnYrs = nyrs - nGuar
    gradRatios = iFixedAnnuity['graduationRatio']**np.arange(nAnnYrs)

    for pState in range(5):
        if pState == 0:
            guarIncomes = np.zeros(nGuar)
        elif pState < 4:
            guarIncomes = guarIncomes_base.copy()
        else:
            guarIncomes = np.cumsum(guarIncomes_base)[::-1]
        annIncomes = iFixedAnnuity['pStateIncomes'][pState] * gradRatios
        psIncomes = np.concatenate([guarIncomes, annIncomes])
        psIncomesM.append(psIncomes)
    psIncomesM = np.array(psIncomesM)
    client['psIncomesM'] = psIncomesM

    incomesM = np.zeros((nscen, nyrs))
    for pState in range(5):
        mat = np.outer(np.ones(nscen), psIncomesM[pState, :])
        ii = np.where(client['pStatesM'] == pState)
        incomesM[ii] = mat[ii]
    client['relIncomesM'] = incomesM

    if iFixedAnnuity['realOrNominal'].lower() == 'n':
        incomesM = incomesM / market['cumCsM']

    pvIncomes = np.sum(incomesM * market['pvsM'])

    feesM = np.zeros((nscen, nyrs))
    annVal = iFixedAnnuity['valueOverCost'] * iFixedAnnuity['cost']
    feesM[:, 0] = iFixedAnnuity['cost'] - annVal

    factor = annVal / pvIncomes
    incomesM = incomesM * factor

    client['incomesM'] = client['incomesM'] + incomesM
    client['feesM'] = client['feesM'] + feesM
    client['budget'] = client['budget'] - iFixedAnnuity['cost']
    client['incomeMSum'] = np.sum(client['incomesM'])
    client['pvIncomes'] = pvIncomes
    return client
