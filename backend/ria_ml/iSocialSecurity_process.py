import numpy as np

def iSocialSecurity_process(iSocialSecurity, client, market):
    nscen, nyrs = client['pStatesM'].shape
    pStatesM = client['pStatesM']
    incomesM = np.zeros((nscen, nyrs))

    # state 3 incomes
    vec = iSocialSecurity['state3Incomes'].flatten()
    if len(vec) > nyrs:
        vec = vec[:nyrs]
    lastval = vec[-1]
    if len(vec) < nyrs:
        vec = np.concatenate([vec, lastval * np.ones(nyrs - len(vec))])
    allIncomes = np.outer(np.ones(nscen), vec)
    states = (pStatesM == 3)
    incomesM += states * allIncomes

    # states 1 and 2
    for s in range(1, 3):
        if s == 1:
            m = iSocialSecurity['state1Incomes'].copy()
        else:
            m = iSocialSecurity['state2Incomes'].copy()
        if m.ndim == 1:
            m = m.reshape(1, -1)
        nrows, ncols = m.shape
        if ncols > nyrs:
            m = m[:, :nyrs]
            ncols = nyrs
        lastcol = m[:, ncols - 1:ncols]
        numadd = nyrs - ncols
        if numadd > 0:
            m = np.hstack([m, np.tile(lastcol, (1, numadd))])

        for i in range(nrows - 1):
            incrow = m[i, :].copy()
            last3col = int(np.sum(np.isinf(incrow)))
            incrow[:last3col] = 0
            psrows = ((pStatesM[:, last3col] == 3) &
                      (pStatesM[:, last3col + 1] == s))
            mm = np.outer(psrows, incrow)
            mm = mm * (pStatesM == s)
            incomesM += mm

        incrow = m[nrows - 1, :].copy()
        last3col = int(np.sum(np.isinf(incrow)))
        incrow[:last3col] = 0
        psrows = (pStatesM[:, last3col] == 3)
        mm = np.outer(psrows, incrow)
        mm = mm * (pStatesM == s)
        incomesM += mm

    client['incomesM'] = client['incomesM'] + incomesM
    return client
