import numpy as np

def iSocialSecurity_process(iSocialSecurity, client, market):
    # creates social security income matrix
    # then adds values to client incomes matrix

    # get number of scenarios and years
    nscen, nyrs = client['pStatesM'].shape

    # save personal states
    pStatesM = client['pStatesM']

    # create social security incomes matrix
    incomesM = np.zeros((nscen, nyrs))

    # add incomes for personal state 3
    # extend input vector
    vec = iSocialSecurity['state3Incomes']
    if len(vec) > nyrs:
        vec = vec[:nyrs]
    lastval = vec[-1]
    vec = np.concatenate((vec, [lastval] * (nyrs - len(vec))))

    # create matrix with incomes for personal state 3
    allIncomes = np.tile(vec, (nscen, 1))
    states = (pStatesM == 3)
    stateIncomes = states * allIncomes

    # add to incomes matrix
    incomesM = incomesM + stateIncomes

    # add incomes for personal states 1 and 2
    for s in [1, 2]:
        # get input matrix
        if s == 1:
            m = iSocialSecurity['state1Incomes']
        else:
            m = iSocialSecurity['state2Incomes']

        # extend input matrix
        nrows, ncols = m.shape
        if ncols > nyrs:
            m = m[:, :nyrs]
            ncols = nyrs
        lastcol = m[:, -1]
        numadd = nyrs - ncols
        if numadd > 0:
            m = np.concatenate((m, np.tile(lastcol, (1, numadd))), axis=1)

        # process all but last row
        for i in range(nrows - 1):
            # get row from matrix
            incrow = m[i, :]
            # find column for last 3
            last3col = np.sum(incrow == np.inf)
            # replace Inf with zero in incrow
            incrow[:last3col] = 0
            # create vector with s in pStateM rows with desired sequence of 3 and s
            psrows = (pStatesM[:, last3col] == 3) & (pStatesM[:, last3col + 1] == s)
            # make matrix with incrow in every eligible row
            mm = np.outer(psrows, incrow)
            # set all cells with state not equal to s to zero
            mm = mm * (pStatesM == s)
            # add to incomes matrix
            incomesM = incomesM + mm

        # process last row
        # get row from matrix
        incrow = m[-1, :]
        # find column for last 3
        last3col = np.sum(incrow == np.inf)
        # replace Inf with zero in incrow
        incrow[:last3col] = 0
        # create vector with 1 in pStateM rows with >= the number of 3s
        psrows = (pStatesM[:, last3col] == 3)
        # make matrix with incrow in every eligible row
        mm = np.outer(psrows, incrow)
        # set all cells with state not equal to s to zero
        mm = mm * (pStatesM == s)
        # add to incomes matrix
        incomesM = incomesM + mm

    # add incomes to client incomes
    client['incomesM'] = client['incomesM'] + incomesM

    return client

