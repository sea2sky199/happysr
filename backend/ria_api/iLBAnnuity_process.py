import numpy as np

def iLBAnnuity_process(iLBAnnuity, client, market):
    # creates LB annuity income matrix and fees matrix
    # then adds values to client incomes matrix and fees matrices

    # get number of scenarios and years
    nscen, nyrs = client['pStatesM'].shape

    # set initial lockbox proportions
    proportions = iLBAnnuity['proportions']

    # reset proportions to adjust for graduation and retention ratios
    gr = iLBAnnuity['graduationRatio']
    rrs = iLBAnnuity['retentionRatios']
    for row in range(2):
        factors = (gr / rrs[row]) ** np.arange(nyrs)
        proportions[row, :] = factors * proportions[row, :]

    # set lockbox proportions to zero for any excluded years
    firstyear = iLBAnnuity['firstIncomeYear']
    if firstyear > 1:
        proportions[:, :firstyear-1] = np.zeros((2, firstyear-1))

    # create matrices of returns net of expenses
    NrfsM = iLBAnnuity['retentionRatios'][0] * market['rfsM']
    NrmsM = iLBAnnuity['retentionRatios'][1] * market['rmsM']

    # create cumulative returns net of expenses
    cumNrfsM = np.hstack((np.ones((nscen, 1)), np.cumprod(NrfsM[:, :nyrs-1], axis=1)))
    cumNrmsM = np.hstack((np.ones((nscen, 1)), np.cumprod(NrmsM[:, :nyrs-1], axis=1)))

    # create matrices with proportions in market and rf in each row
    xfm = np.outer(np.ones(nscen), proportions[0, :])
    xmm = np.outer(np.ones(nscen), proportions[1, :])

    # compute net incomes for lockbox relative proportions
    boxIncsM = xfm * cumNrfsM + xmm * cumNrmsM

    # compute incomes if there were no expenses
    gboxIncsM = xfm * market['cumRfsM'] + xmm * market['cumRmsM']

    # set fees to differences
    feesM = gboxIncsM - boxIncsM

    # set up relative incomes matrix and relative fees matrix
    psRelIncs = iLBAnnuity['pStateRelativeIncomes']
    psRelIncs = psRelIncs / np.max(psRelIncs)
    relIncsM = np.zeros((nscen, nyrs))
    relFeesM = np.zeros((nscen, nyrs))
    for ps in range(1, 5):
        relInc = psRelIncs[ps-1]
        psmat = (client['pStatesM'] == ps)
        psIncsM = relInc * (psmat * boxIncsM)
        relIncsM += psIncsM
        psFeesM = relInc * (psmat * feesM)
        relFeesM += psFeesM

    # convert relative incomes to dollar incomes
    pvbase = np.sum(np.sum((relIncsM + relFeesM) * market['pvsM']))
    totval = iLBAnnuity['cost'] * iLBAnnuity['valueOverCost']
    incsM = relIncsM * (totval / pvbase)
    feesM = relFeesM * (totval / pvbase)

    # add incomes and fees to client incomes and fees matrices
    client['incomesM'] += incsM
    client['feesM'] += feesM

    # add insurance fee to fee matrix
    insFee = iLBAnnuity['cost'] * (1 - iLBAnnuity['valueOverCost'])
    client['feesM'][:, 0] += insFee



