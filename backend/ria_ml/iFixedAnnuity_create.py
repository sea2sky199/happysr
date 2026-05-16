def iFixedAnnuity_create():
    iFixedAnnuity = {}
    iFixedAnnuity['guaranteedIncomes'] = []
    iFixedAnnuity['pStateIncomes'] = [0, 0.5, 0.5, 1, 0]
    iFixedAnnuity['graduationRatio'] = 1.00
    iFixedAnnuity['realOrNominal'] = 'r'
    iFixedAnnuity['valueOverCost'] = 0.90
    iFixedAnnuity['cost'] = 100000
    return iFixedAnnuity
