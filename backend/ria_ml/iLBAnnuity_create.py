def iLBAnnuity_create():
    iLBAnnuity = {}
    iLBAnnuity['proportions'] = []
    iLBAnnuity['firstIncomeYear'] = 1
    iLBAnnuity['pStateRelativeIncomes'] = [0.5, 0.5, 1.0, 0]
    iLBAnnuity['graduationRatio'] = 1.00
    iLBAnnuity['retentionRatios'] = [0.999, 0.999]
    iLBAnnuity['valueOverCost'] = 0.90
    iLBAnnuity['cost'] = 100000
    return iLBAnnuity
