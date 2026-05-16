import numpy as np

def iLBAnnuity_process(iLBAnnuity, client, market):
    nscen, nyrs = client['pStatesM'].shape
    proportions = np.array(iLBAnnuity['proportions'], dtype=float)

    gr = iLBAnnuity['graduationRatio']
    rrs = iLBAnnuity['retentionRatios']
    for row in range(2):
        factors = (gr / rrs[row])**np.arange(nyrs)
        proportions[row, :] = factors * proportions[row, :]

    firstyear = iLBAnnuity['firstIncomeYear']
    if firstyear > 1:
        proportions[:, :firstyear - 1] = 0

    NrfsM = rrs[0] * market['rfsM']
    NrmsM = rrs[1] * market['rmsM']
    m = np.cumprod(NrfsM, axis=1)
    cumNrfsM = np.hstack([np.ones((nscen, 1)), m[:, :-1]])
    m = np.cumprod(NrmsM, axis=1)
    cumNrmsM = np.hstack([np.ones((nscen, 1)), m[:, :-1]])

    xfm = np.outer(np.ones(nscen), proportions[0, :])
    xmm = np.outer(np.ones(nscen), proportions[1, :])
    boxIncsM = xfm * cumNrfsM + xmm * cumNrmsM
    gboxIncsM = xfm * market['cumRfsM'] + xmm * market['cumRmsM']
    feesM = gboxIncsM - boxIncsM

    psRelIncs = np.array(iLBAnnuity['pStateRelativeIncomes'], dtype=float)
    psRelIncs = psRelIncs / np.max(psRelIncs)
    relIncsM = np.zeros((nscen, nyrs))
    relFeesM = np.zeros((nscen, nyrs))
    for ps in range(1, 5):
        relInc = psRelIncs[ps - 1]
        psmat = (client['pStatesM'] == ps)
        relIncsM += relInc * (psmat * boxIncsM)
        relFeesM += relInc * (psmat * feesM)

    pvbase = np.sum((relIncsM + relFeesM) * market['pvsM'])
    totval = iLBAnnuity['cost'] * iLBAnnuity['valueOverCost']
    incsM = relIncsM * (totval / pvbase)
    feesM = relFeesM * (totval / pvbase)

    client['incomesM'] = client['incomesM'] + incsM
    client['feesM'] = client['feesM'] + feesM
    insFee = iLBAnnuity['cost'] * (1 - iLBAnnuity['valueOverCost'])
    client['feesM'][:, 0] += insFee
    return client
