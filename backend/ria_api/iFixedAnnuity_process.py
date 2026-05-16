import numpy as np


def iFixedAnnuity_process(iFixedAnnuity, client, market):
    # creates fixed annuity income matrix and fees matrix
    # then adds values to client incomes matrix and fees matrices

    # get number of scenarios and years
    nscen, nyrs = client['pStatesM'].shape
    
    # make matrix of incomes for states 0,1,2,3 and 4
    psIncomesM = []
    for pState in range(5):
        # guaranteed incomes 
        if pState == 0:
            guarIncomes = np.zeros(len(iFixedAnnuity['guaranteedIncomes']))
        elif 0 < pState < 4:
            guarIncomes = iFixedAnnuity['guaranteedIncomes']
        else:  # pState == 4
            guarIncomes = np.flip(np.cumsum(iFixedAnnuity['guaranteedIncomes']))
        
        # annuity incomes
        nAnnYrs = nyrs - len(iFixedAnnuity['guaranteedIncomes'])
        gradRatios = iFixedAnnuity['graduationRatio'] ** np.arange(nAnnYrs)
        annIncomes = iFixedAnnuity['pStateIncomes'][pState] * gradRatios
        
        # guaranteed and annuity incomes
        psIncomes = np.concatenate((guarIncomes, annIncomes))
        # add to matrix
        psIncomesM.append(psIncomes)
    
    psIncomesM = np.array(psIncomesM)

    # create matrix of relative incomes for all scenarios
    incomesM = np.zeros((nscen, nyrs))
    for pState in range(5):
        # make matrix of incomes for personal state
        mat = np.ones((nscen, 1)) * psIncomesM[pState, :]
        # find cells in client personal state matrix for this state
        ii = np.where(client['pStatesM'] == pState)[0]
        # put selected incomes in incomes Matrix
        incomesM[ii] = mat[ii]
    
    # if values are nominal, change to real
    if iFixedAnnuity['realOrNominal'].lower() == 'n':
        incomesM /= market['cumCsM']
    
    # compute present value of all relative incomes
    pvIncomes = np.sum(incomesM * market['pvsM'])
    
    # create fee matrix  
    feesM = np.zeros((nscen, nyrs))
    # compute value of annuity purchased 
    annVal = iFixedAnnuity['valueOverCost'] * iFixedAnnuity['cost']
    # add fee to matrix in column 1
    feesM[:, 0] = iFixedAnnuity['cost'] - annVal
    
    # scale incomes so pv = amount invested - fee
    factor = annVal / pvIncomes
    incomesM *= factor
    
    # add incomes and fees to client matrices
    client['incomesM'] += incomesM
    client['feesM'] += feesM
    # subtract cost from client budget
    client['budget'] -= iFixedAnnuity['cost']
    return client

